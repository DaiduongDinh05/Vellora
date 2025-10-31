import { Text, View, TextInput, TouchableOpacity, KeyboardTypeOptions } from 'react-native'
import React, {useState} from 'react'
import { FontAwesome } from '@expo/vector-icons'

type Props = {
    label: string;
    value: string;
    onChangeText: (text: string) => void;
    unit: '$' | 'mi';
}
const EditableNumericDisplay: React.FC<Props> = ({ label, value, onChangeText, unit }) => {
    const [isEditing, setIsEditing] = useState(false);

    let keyboardType: KeyboardTypeOptions = 'numeric';
    let prefix = '';
    let suffix = '';

    if (unit == '$'){
        keyboardType = 'decimal-pad';
        prefix = '$';
    }
    else {
        suffix = ' mi';
    }

    const handleTextChange = (text: string) => {
        let formattedText = text;
        if (unit == '$'){
            formattedText = text.replace(/[^0-9.]/g, '');

            const parts = formattedText.split('.');
            if (parts.length > 2){
                onChangeText(value);
                return;
            }
        }
        else {
            formattedText = text.replace(/[^0-9]/g, '');
        }
        onChangeText(formattedText);
    };

    const handleBlur = () => {
        setIsEditing(false);
        if (unit == '$'){
            const num = parseFloat(value) || 0;
            onChangeText(num.toFixed(2));
        }
    };

    return (
        <View className='flex-row items-center gap-2'>
            {isEditing ? (
                <View className='flex-row items-baseline border-b border-gray-300'>
                    <Text className='text-xl'>{label} : {prefix}</Text>
                    <TextInput 
                        value={value}
                        onChangeText={handleTextChange}
                        keyboardType={keyboardType}
                        onBlur={handleBlur}
                        autoFocus={true}
                        className='text-xl font-bold py-0 px-1 w-24'
                    />
                    <Text className='text-xl font-bold'>{suffix}</Text>
                </View>
            ) : (
                <View className='flex-row items-center gap-2'>
                    <Text className='text-xl'>{label}: {' '}
                        <Text className='font-bold'>{prefix}{value}{suffix}</Text>
                    </Text>
                    <TouchableOpacity onPress={() => setIsEditing(true)}>

                        <FontAwesome name='pencil' size={18} color="#6B7280"></FontAwesome>
                    </TouchableOpacity>
                </View>

            )}
        </View>
    )
}

export default EditableNumericDisplay
