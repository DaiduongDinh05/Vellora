import { StyleSheet, View } from 'react-native'
import React from 'react'
import RNPickerSelect from 'react-native-picker-select'
import { FontAwesome } from '@expo/vector-icons';

const Dropdown = ({ 
    items = [], 
    onValueChange, 
    placeholder = "Select an option", // default prompt 
    value, 
    icon 
  }: {
    items?: {label: string, value: string | number}[];
    onValueChange: (value: string | null) => void;
    placeholder?: string;
    value: string | number | null;
    icon?: React.ReactNode;
  }) => {

  return (
    <View className="flex-row border items-center border-gray-300 bg-white rounded-lg px-3 py-3">
      <View className='w-6 items-center'>
        {icon}
      </View>
        <RNPickerSelect 
            onValueChange={onValueChange}
            items = {items}
            value={value}
            placeholder={placeholder ? { label: placeholder, value: null } : {}}
            style={pickerSelectStyles}

            Icon={() => {
              return <FontAwesome name="chevron-down" size={12}/>
            }}
        />
            
    </View>
  )
}

const pickerSelectStyles = StyleSheet.create({
  inputIOS: {
    fontSize: 16,
    borderRadius: 8,
    color: 'black',
    backgroundColor: 'white',
    paddingRight: 30, // to ensure the text is never behind the icon
    marginBottom: 14,
    flex: 1,
    marginLeft: 8,

  },
  inputAndroid: {
    fontSize: 16,
    borderRadius: 8,
    color: 'black',
    backgroundColor: 'white',
    paddingRight: 30, // to ensure the text is never behind the icon
  },
  placeholder: {
    color: 'gray',
  },
  iconContainer: {
    top: '50%',
    marginTop: -12,
    right: 15,
  },
  inputIOSContainer: {
    zIndex: 100,
  },

});

export default Dropdown

