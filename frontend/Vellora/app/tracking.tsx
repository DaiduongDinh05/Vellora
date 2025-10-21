import { StyleSheet, Text, View } from 'react-native'
import React, { useState } from 'react'
import RNPickerSelect from 'react-native-picker-select'
import { SafeAreaView } from 'react-native-safe-area-context';
import NoteInput from './components/NoteInput'
// export const Dropdown = () => {
//   return (
    
//   )
// }

const Tracking = () => {

    const [value, setValue] = useState(null);
    const [notes, setNotes] = useState('');
  return (
    <SafeAreaView style={{flex: 1}}>
        <View style={{flex:1, padding: 20}}>
            <Text>tracking</Text>
            
            <NoteInput 
                placeholder="Add your crazy notes"
                value={notes}
                onChangeText={setNotes}
                className=''
            />
            <RNPickerSelect 
                onValueChange={(value) => setValue(value)}
                items = {[
                    {label: 'Test1', value: 'test1'},
                    {label: 'Test2', value: 'test2'},
                    {label: 'Test3', value: 'test3'},

                ]}
                value={value}
                placeholder={{label: 'Select something...', value: null}}
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
    </SafeAreaView>


    
  )
}

export default Tracking

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