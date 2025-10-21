import { StyleSheet, Text, View } from 'react-native'
import React, { useState } from 'react'
import RNPickerSelect from 'react-native-picker-select'
import { SafeAreaView } from 'react-native-safe-area-context';
import NoteInput from './components/NoteInput'
import Dropdown from './components/Dropdown'

const Tracking = () => {

  const [value, setValue] = useState(null);
  const [notes, setNotes] = useState('');
  const [vehicle, setVehicle] = useState(null);

  const vehicleItems = [
    {label: 'Personal Car (Toyota)', value: 'toyota'},
    {label: 'Business Car (Mazda)', value: 'mazda'},
    {label: 'Random Car (Nissan)', value: 'nissan'},

  ]
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
            <Dropdown 
              placeholder="Select vehicle"
              items={vehicleItems}
              onValueChange={setVehicle}
              value={vehicle}
            
            />
            
        </View>
    </SafeAreaView>

  )
}

export default Tracking
