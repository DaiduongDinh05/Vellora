import { StyleSheet, Text, View, TextInput } from 'react-native'
import React from 'react'

type CurrencyInputProps = {
    label: string;
    value: string;
    onChangeText: (text: string) => void;
    className?: string;
}
const CurrencyInput: React.FC<CurrencyInputProps> = ({
    label,
    value,
    onChangeText,
    className = ''
}) => {

    const handleTextChange = (text: string) => {

        const formattedText = text.replace(/[^0-9.]/g, '');
        const parts = formattedText.split('.');

        if (parts.length > 2){
            onChangeText(value);
            return;
        }

        onChangeText(formattedText);
    };
    
    return (
        <View className={`flex-1 ${className}`}>
            <Text>{label}</Text>
            <View className='border'>
                <Text>$</Text>
                <TextInput 
                    className='text-base text-black'
                    placeholder="0.00"
                    editable
                    value={value}
                    onChangeText={handleTextChange}
                    keyboardType="numeric"
                
                />
            </View>
        </View>
    )
}

export default CurrencyInput

// const styles = StyleSheet.create({})