import { StyleSheet, Text, View, TextInput, TouchableOpacity, KeyboardTypeOptions } from 'react-native'
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

    return (
        <View>
        <Text>EditableNumericDisplay</Text>
        </View>
    )
}

export default EditableNumericDisplay

const styles = StyleSheet.create({})