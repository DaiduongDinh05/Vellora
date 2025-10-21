import React from 'react';
import { TextInput } from 'react-native';

const NoteInput = ({ className = '', ...props }) => {
    return (
        <TextInput
            // add styles through classname. Append other passed classNames
            className={`text-base py-3 px-2.5 border border-gray-500 rounded-lg text-black bg-white pr-8 mb-4 h-24 ${className}`}
            textAlignVertical='top'
            editable
            multiline
            numberOfLines={4}
            maxLength={300} // limit max characters
            placeholderTextColor="#9a9a9a"
            {...props}
        />
    );
};

export default NoteInput;
