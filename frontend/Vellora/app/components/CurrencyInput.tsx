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

        if (text == ''){
            onChangeText('');
            return;
        }

        if (parts.length > 2){
            onChangeText(value);
            return;
        }

        if (parts[1] && parts[1].length > 2){
            onChangeText(value);
            return;
        }

        onChangeText(formattedText);
    };

    const handleFormatting = () => {

        if (value == '' || value == '.' || value == '0'){
            onChangeText('0.00');
            return;
        }

        const num = parseFloat(value);

        if (!isNaN(num)){
            onChangeText(num.toFixed(2));
        }
    };
    
    return (
        <View className={`w-20 flex-none ${className}`}>
            <Text className='text-sm text-gray-500 mb-1'>{label}</Text>
            <View className={`flex-row py-3 px-2.5 items-center border border-gray-300 rounded-lg text-black bg-white ${className}`}>
                <Text className='text-base text-black font-bold w-5'>$</Text>
                <TextInput 
                    className=""
                    placeholderTextColor='gray'
                    placeholder="0.00"
                    editable
                    value={value}
                    onChangeText={handleTextChange}
                    onEndEditing={handleFormatting}
                    keyboardType="numeric"
                
                />
            </View>
        </View>
    )
}

export default CurrencyInput

// const styles = StyleSheet.create({})