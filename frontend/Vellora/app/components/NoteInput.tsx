import React from 'react';
import { TextInput, TextInputProps } from 'react-native';

// define prop types by extending the standard textinputprops
type NoteInputProps = TextInputProps & {
    className?: string;
}

const NoteInput: React.FC<NoteInputProps> = ({ className = '', ...props }) => {
    return (
        <TextInput
            // add base styles through classname. Append other passed classNames
            className={`text-base py-3 px-2.5 border border-gray-300 rounded-lg text-black bg-white pr-8 h-24 ${className}`}
            textAlignVertical='top'     // keep text at the top
            editable
            multiline
            maxLength={300}             // limit max characters
            placeholderTextColor='gray'
            {...props}                  // pass all other props
        />
    );
};

export default NoteInput;
