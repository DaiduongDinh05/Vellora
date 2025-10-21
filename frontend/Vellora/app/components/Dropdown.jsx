import { StyleSheet, Text, View } from 'react-native'
import React from 'react'
import RNPickerSelect from 'react-native-picker-select'

const Dropdown = ({ items, onValueChange, placeholder, value, icon }) => {
  return (
    <View className="bg-gray-100 rounded-lg-mb-4">
        {icon}
        <RNPickerSelect 
            onValueChange={onValueChange}
            items = {items}
            value={value}
            placeholder={placeholder ? { label: placeholder, value: null } : {}}
            style={pickerSelectStyles}

            pickerProps={{
                itemStyle: {
                    color: 'black',
                }
            }}
                
        />

        {value && (
            <Text>You selected: {value}</Text>
        )}
            
    </View>
  )
}

export default Dropdown


const pickerSelectStyles = StyleSheet.create({
  inputIOS: {
    fontSize: 16,
    paddingVertical: 12,
    paddingHorizontal: 10,
    borderWidth: 1,
    borderColor: 'gray',
    borderRadius: 8,
    color: 'black',
    backgroundColor: 'white',
    paddingRight: 30, // to ensure the text is never behind the icon
    marginBottom: 14
  },
  inputAndroid: {
    fontSize: 16,
    paddingHorizontal: 10,
    paddingVertical: 8,
    borderWidth: 1,
    borderColor: 'gray',
    borderRadius: 8,
    color: 'black',
    backgroundColor: 'white',
    paddingRight: 30, // to ensure the text is never behind the icon
  },
  placeholder: {
    color: 'gray',
  },
  inputIOSContainer: {
    zIndex: 100,
  },
});