import { StyleSheet, Text, View, TextInput, TextInputProps } from 'react-native'
import React from 'react'

type FilledAddressBoxProps = TextInputProps & {
    className?: string;
}

const FilledAddressBox: React.FC<FilledAddressBoxProps> = ({className = '', ...props}) => {
  return (
    <TextInput 
        className={`
            text-base py-3 px-2.5 border border-gray-300
            rounded-lg text-black bg-white
            ${className}
        `}
        placeholderTextColor='gray'
        {...props}
    
    />

  );
}

export default FilledAddressBox;

const styles = StyleSheet.create({})