import re
import ipaddress

from typing import Optional, List
from pydantic import BaseModel

from app.converter.core.exceptions.iocs import IocsLimitExceededException, EmptyIOCSException
from app.converter.tools.const import IP_IOC_REGEXP_PATTERN, DOMAIN_IOC_REGEXP_PATTERN, URL_IOC_REGEXP_PATTERN, \
    hash_regexes, IOCType, HashType, IocParsingRule, HASH_MAP


class Iocs(BaseModel):
    ip: list[str] = []
    url: list[str] = []
    domain: list[str] = []
    hash_dict: dict = {}

    def get_total_count(self) -> int:
        hash_len = 0
        for value in self.hash_dict.values():
            hash_len += len(value)
        return len(self.ip) + len(self.url) + len(self.domain) + hash_len

    def return_iocs(self) -> dict:
        if all(not value for value in [self.ip, self.url, self.domain, self.hash_dict]):
            raise EmptyIOCSException()
        result = {"DestinationIP": self.ip, "URL": self.url, "Domain": self.domain}
        for key, value in self.hash_dict.items():
            result[HASH_MAP[key]] = value
        return result


class CTIParser:

    def get_iocs_from_string(
        self,
        string: str,
        include_ioc_types: Optional[List[IOCType]] = None,
        include_hash_types: Optional[List[HashType]] = None,
        exceptions: Optional[List[str]] = None,
        ioc_parsing_rules: Optional[List[IocParsingRule]] = None,
        limit: Optional[int] = None
    ) -> Iocs:
        iocs = Iocs()
        string = self.replace_dots_hxxp(string, ioc_parsing_rules)
        if not include_ioc_types or "ip" in include_ioc_types:
            iocs.ip.extend(self._find_all_str_by_regex(string, IP_IOC_REGEXP_PATTERN))
        if not include_ioc_types or "domain" in include_ioc_types:
            iocs.domain.extend(self._find_all_str_by_regex(string, DOMAIN_IOC_REGEXP_PATTERN))
        if not include_ioc_types or "url" in include_ioc_types:
            iocs.url.extend(self._find_all_str_by_regex(string, URL_IOC_REGEXP_PATTERN))
        if not include_ioc_types or "hash" in include_ioc_types:
            if not include_hash_types:
                include_hash_types = list(hash_regexes.keys())
            for hash_type in include_hash_types:
                iocs.hash_dict[hash_type] = self._find_all_str_by_regex(string, hash_regexes[hash_type])
        iocs = self.remove_duplicates(iocs)
        iocs = self.remove_exceptions(iocs, exceptions)
        if ioc_parsing_rules is None or "remove_private_and_reserved_ips" in ioc_parsing_rules:
            self._exclude_private_and_reserved_ips(iocs)
        if limit is not None:
            total_count = iocs.get_total_count()
            if total_count > limit:
                raise IocsLimitExceededException(f"IOCs count {total_count} exceeds limit {limit}.")
        return iocs.return_iocs()

    def replace_dots_hxxp(self, string, ioc_parsing_rules):
        if ioc_parsing_rules is None or "replace_dots" in ioc_parsing_rules:
            string = self._replace_dots(string)
        if ioc_parsing_rules is None or "replace_hxxp" in ioc_parsing_rules:
            string = self._replace_hxxp(string)
        return string

    def remove_duplicates(self, iocs):
        iocs.ip = self._remove_duplicates_from_list(iocs.ip)
        iocs.domain = self._remove_duplicates_from_list(iocs.domain)
        iocs.url = self._remove_duplicates_from_list(iocs.url)
        for key, value in iocs.hash_dict.items():
            iocs.hash_dict[key] = self._remove_duplicates_from_list(value)
        return iocs

    def remove_exceptions(self, iocs, exceptions=None):
        iocs.ip = self._remove_exceptions(iocs.ip, exceptions)
        iocs.domain = self._remove_exceptions(iocs.domain, exceptions)
        iocs.url = self._remove_exceptions(iocs.url, exceptions)
        for key, value in iocs.hash_dict.items():
            iocs.hash_dict[key] = self._remove_exceptions(value, exceptions)
        return iocs

    @staticmethod
    def _find_all_str_by_regex(s: str, pattern: str) -> list[str]:
        return re.findall(pattern, s, re.MULTILINE)

    @staticmethod
    def _remove_duplicates_from_list(ls: list) -> list:
        return list(dict.fromkeys(ls))

    @classmethod
    def _remove_exceptions(
        cls, values: list[str], exceptions: Optional[List[str]]
    ) -> list[str]:
        if not exceptions:
            return values
        return [v for v in values if not cls._str_contain_one_of_exceptions(v, exceptions)]

    @staticmethod
    def _str_contain_one_of_exceptions(s: str, exceptions: list[str]) -> bool:
        for e in exceptions:
            if e in s:
                return True
        return False

    @staticmethod
    def _replace_dots(s: str) -> str:
        s = s.replace("(.)", ".")
        s = s.replace("[.]", ".")
        s = s.replace("{.}", ".")
        return s

    @staticmethod
    def _replace_hxxp(s: str) -> str:
        return s.replace("hxxp", "http")

    @classmethod
    def _exclude_private_and_reserved_ips(cls, iocs: Iocs) -> None:
        iocs.ip = [ip for ip in iocs.ip if not cls._is_private_or_reserved(ip)]

    @staticmethod
    def _is_private_or_reserved(ip: str) -> bool:
        try:
            addr = ipaddress.ip_address(ip)
            return addr.is_private or addr.is_reserved
        except Exception:
            return False
