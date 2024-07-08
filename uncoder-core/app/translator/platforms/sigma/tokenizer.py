"""
Uncoder IO Commercial Edition License
-----------------------------------------------------------------
Copyright (c) 2024 SOC Prime, Inc.

This file is part of the Uncoder IO Commercial Edition ("CE") and is
licensed under the Uncoder IO Non-Commercial License (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://github.com/UncoderIO/UncoderIO/blob/main/LICENSE

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-----------------------------------------------------------------
"""

import re
from typing import Union

from app.translator.core.custom_types.tokens import GroupType, LogicalOperatorType
from app.translator.core.exceptions.parser import TokenizerGeneralException
from app.translator.core.models.query_tokens.field_value import FieldValue
from app.translator.core.models.query_tokens.keyword import Keyword
from app.translator.core.models.query_tokens.identifier import Identifier
from app.translator.platforms.sigma.models.modifiers import ModifierManager


class Selection:
    token_type = "selection"

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Selection({self.name})"


class SigmaTokenizer:
    modifier_manager = ModifierManager()

    def __init__(self):
        self.supported_selection_types = {dict: self.__parse_and_selection, list: self.__parse_or_selection}

    def __parse_field(self, field_name: str, values: Union[int, str, list[Union[int, str]]]) -> Union[list, FieldValue]:
        field_name, *modifier = field_name.split("|") if "|" in field_name else (field_name, "=")
        return self.modifier_manager.generate(field_name=field_name, modifier=modifier, value=values)

    @staticmethod
    def __parse_keyword(values):
        return (Keyword(value=values),)

    def __parse_and_selection(self, selection: dict):
        result = []
        for field, values in selection.items():
            token = self.__parse_field(field_name=field, values=values)
            result.extend((*token, Identifier(token_type=LogicalOperatorType.AND)))
        return [Identifier(token_type=GroupType.L_PAREN), *result[:-1], Identifier(token_type=GroupType.R_PAREN)]

    def __parse_or_selection(self, selection: list):
        result = []
        for field_values in selection:
            field, values = next(iter(field_values.items()))
            token = self.__parse_field(field_name=field, values=values)
            result.extend((*token, Identifier(token_type=LogicalOperatorType.OR)))
        return [Identifier(token_type=GroupType.L_PAREN), *result[:-1], Identifier(token_type=GroupType.R_PAREN)]

    def __get_one_field_tokenized(self, selection: Union[dict, list]):
        if isinstance(selection, dict):
            field, value = next(iter(selection.items()))
            return self.__parse_field(field_name=field, values=value)
        elif isinstance(selection, list) and all(isinstance(i, dict) for i in selection):
            field, value = next(iter(selection[0].items()))
            return self.__parse_field(field_name=field, values=value)
        else:
            return self.__parse_keyword(values=selection)

    def __parse_selection(self, selection: Union[dict, list]):
        if len(selection) == 1 and type(selection) in self.supported_selection_types:
            return self.__get_one_field_tokenized(selection=selection)
        if isinstance(selection, list) and all(isinstance(i, str) for i in selection):
            return self.__parse_keyword(selection)
        if selection_method := self.supported_selection_types.get(type(selection)):
            return selection_method(selection=selection)
        raise Exception("Unsupported sigma type")

    def tokenize(self, detection: dict) -> list:
        condition = detection.pop("condition")
        condition_tokens = SigmaConditionTokenizer().tokenize(condition=condition, detection=detection)
        tokenized = []
        for token in condition_tokens:
            if isinstance(token, Selection):
                selection_values = detection.get(token.name)
                selection = self.__parse_selection(selection=selection_values)
                tokenized.extend(selection)
            else:
                tokenized.append(token)
        return tokenized


class SigmaConditionTokenizer:
    logical_operator_pattern = r"\s?(?P<logical_operator>and|or|not)\s?"
    selection_pattern = r"(?P<selection_name>[$a-zA-Z\._\-0-9]+)"
    multi_selection_pattern = r"(?P<selection_pattern>[$a-zA-Z\._\-0-9]+)(?:\*){1}"
    one_of_selection = "1 of "
    all_of_selection = "all of "

    def __init__(self):
        self.detection = {}

    def __get_selection(self, condition: str) -> tuple[Selection, str]:
        selection_search = re.search(self.selection_pattern, condition)
        if selection_search is None:
            raise TokenizerGeneralException(error=f"Selection couldn't be found in condition: {condition}")
        selection = selection_search.group("selection_name")
        pos = selection_search.end()
        return Selection(name=selection), condition[pos:]

    def __get_group(self, condition: str, operator: Identifier) -> tuple[list, str]:
        selection_pattern_search = re.search(self.multi_selection_pattern, condition)
        if selection_pattern_search is None:
            raise TokenizerGeneralException(error=f"Selection couldn't be found in condition: {condition}")
        selection_pattern = selection_pattern_search.group("selection_pattern")
        pos = selection_pattern_search.end()
        tokens = []
        for selection in self.detection:
            if selection.startswith(selection_pattern):
                tokens.append(Selection(name=selection))
                tokens.append(operator)
        return [
            Identifier(token_type=GroupType.L_PAREN),
            *tokens[:-1],
            Identifier(token_type=GroupType.R_PAREN),
        ], condition[pos:]

    @staticmethod
    def get_missed_parentheses(tokens: list[Union[Selection, Identifier]]) -> list[int]:
        missed_indices = []
        for index in range(len(tokens) - 1):
            token = tokens[index]
            next_token = tokens[index + 1]
            if token.token_type == LogicalOperatorType.NOT and next_token.token_type != GroupType.L_PAREN:
                missed_indices.append(index + 1)
        return missed_indices

    def __add_parentheses_after_and_not(
        self, tokens: list[Union[Selection, Identifier]]
    ) -> list[Union[Selection, Identifier]]:
        indices = self.get_missed_parentheses(tokens=tokens)
        for index in reversed(indices):
            tokens.insert(index + 1, Identifier(token_type=GroupType.R_PAREN))
            tokens.insert(index, Identifier(token_type=GroupType.L_PAREN))
        return tokens

    def __get_identifier(
        self, condition: str
    ) -> Union[tuple[Identifier, str], tuple[list, str], tuple[Selection, str]]:
        condition = condition.strip("\n").strip(" ").strip("\n")
        if condition.startswith(GroupType.L_PAREN):
            return Identifier(token_type=GroupType.L_PAREN), condition[1:]
        if condition.startswith(GroupType.R_PAREN):
            return Identifier(token_type=GroupType.R_PAREN), condition[1:]
        if logical_operator_search := re.match(self.logical_operator_pattern, condition, re.IGNORECASE):
            logical_operator = logical_operator_search.group("logical_operator")
            pos = logical_operator_search.end()
            return Identifier(token_type=logical_operator.lower()), condition[pos:]
        if condition.startswith(self.one_of_selection):
            condition = re.sub(self.one_of_selection, "", condition, 1)
            return self.__get_group(condition=condition, operator=Identifier(token_type=LogicalOperatorType.OR))
        if condition.startswith(self.all_of_selection):
            condition = re.sub(self.all_of_selection, "", condition, 1)
            return self.__get_group(condition=condition, operator=Identifier(token_type=LogicalOperatorType.AND))
        return self.__get_selection(condition)

    def tokenize(self, condition: str, detection: dict) -> list:
        self.detection = detection
        tokenized = []
        while condition:
            identifier, condition = self.__get_identifier(condition=condition)
            if isinstance(identifier, list):
                tokenized.extend(identifier)
            else:
                tokenized.append(identifier)
        return self.__add_parentheses_after_and_not(tokens=tokenized)
