import { StyleSheet, View } from 'react-native'
import React from 'react'
import RNPickerSelect from 'react-native-picker-select'
import { FontAwesome } from '@expo/vector-icons';

// Define component prop types
type DropdownProps = {
  items?: {label: string, value: string | number}[];
  onValueChange: (value: string | null) => void;
  placeholder?: string;
  value: string | number | null;
  icon?: React.ReactNode;
  className?: string;
}
const Dropdown: React.FC<DropdownProps> = ({
  items = [], 
  onValueChange, 
  placeholder = "Select an option", // default prompt 
  value, 
  icon,
  className = ''
}) => {

  // conditionally add margin if an icon exists
  const dynamicPickerStyles = {
    ...pickerSelectStyles,
    inputIOS: [
      pickerSelectStyles.inputIOS,
      icon ? { marginLeft: 10 } : {},
    ],
    inputAdroid: [
      pickerSelectStyles.inputAndroid,
      icon ? { marginLeft: 10 } : {},
    ],
  }
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
        style={dynamicPickerStyles}
        pickerProps={{
          itemStyle: {
            color: 'black',
          }
        }}
        Icon={() => {
          return <FontAwesome name="chevron-down" size={12}/>
        }}

      />      
    </View>
  )
}

const pickerSelectStyles = StyleSheet.create({

  viewContainer: {
    flex: 1,
  },

  inputIOS: {
    fontSize: 16,
    borderRadius: 8,
    color: 'black',
    backgroundColor: 'white',
    paddingRight: 30, // to ensure the text is never behind the icon
    flex: 1,
  },

  inputAndroid: {
    fontSize: 16,
    borderRadius: 8,
    color: 'black',
    backgroundColor: 'white',
    paddingRight: 30, // to ensure the text is never behind the icon
    flex: 1,
  },
  placeholder: {
    color: 'gray',
  },
  iconContainer: {
    top: '50%',
    marginTop: -6,
    right: 15,
  },
  inputIOSContainer: {
    zIndex: 100,
  },

});

export default Dropdown

