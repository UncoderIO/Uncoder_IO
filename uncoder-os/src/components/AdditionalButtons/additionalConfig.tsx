import React from 'react';
import { AdditionalButtonNames } from '../../enums';

import { ReactComponent as RootaIcon } from './Svg/RootaIcon.svg';
// import { ReactComponent as DockerIcon } from './Svg/DockerIcon.svg';
import { ReactComponent as GitHubIcon } from './Svg/GitHubIcon.svg';
import { ReactComponent as DiscordIcon } from './Svg/DiscordIcon.svg';
import { ReactComponent as GuideIcon } from './Svg/GuideIcon.svg';

export type AdditionalType = {
  icon: React.ReactNode;
  text: string;
  classes?: AdditionalButtonNames;
  href?: string | undefined;
  target?: string | undefined;
  disabled?: boolean;
  handleClick?: () => void;
};

export const additionalConfig: AdditionalType[] = [
  {
    icon: <RootaIcon/>,
    text: 'What is RootA',
    classes: AdditionalButtonNames.Roota,
    href: 'https://roota.io',
    target: '_blank',
  },
  /* {
    icon: <DockerIcon/>,
    text: AdditionalButtonNames.Docker,
    href: '#',
    target: '_blank',
  }, */
  {
    icon: <GitHubIcon/>,
    text: AdditionalButtonNames.GitHub,
    classes: AdditionalButtonNames.GitHub,
    href: 'https://github.com/UncoderIO/UncoderIO',
    target: '_blank',
  },
  {
    icon: <DiscordIcon/>,
    text: AdditionalButtonNames.Community,
    classes: AdditionalButtonNames.Community,
    href: 'https://discord.gg/socprime',
    target: '_blank',
  },
  {
    icon: <GuideIcon/>,
    text: AdditionalButtonNames.Guide,
    classes: AdditionalButtonNames.Guide,
    href: 'https://github.com/UncoderIO/UncoderIO/blob/main/README.md',
    target: '_blank',
  },
];
