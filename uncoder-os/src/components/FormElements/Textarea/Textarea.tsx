import React, {
  DetailedHTMLProps, FC, TextareaHTMLAttributes,
} from 'react';

import './Textarea.sass';

interface TextareaPropsType extends
  DetailedHTMLProps<TextareaHTMLAttributes<HTMLTextAreaElement>, HTMLTextAreaElement> {
  classes?: string;
}

export const Textarea: FC<TextareaPropsType> = ({ classes, ...props }) => (
  <div className={`textarea-grid ${classes ?? ''}`}>
    <textarea className="textarea-grid__input" {...props}></textarea>
  </div>
);
