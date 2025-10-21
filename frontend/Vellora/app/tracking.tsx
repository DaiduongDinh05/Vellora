import { StyleSheet, Text, View } from 'react-native'
import React, { useState } from 'react'
import RNPickerSelect from 'react-native-picker-select'
import { SafeAreaView } from 'react-native-safe-area-context';
import NoteInput from './components/NoteInput'
import Dropdown from './components/Dropdown'
import { ScrollView } from 'react-native';
import { FontAwesome } from '@expo/vector-icons';

const Tracking = () => {

  // state variables
  const [notes, setNotes] = useState('');
  const [vehicle, setVehicle] = useState(null);
  const [type, setType] = useState(null);
  const [rate, setRate] = useState(null);

  // common style for icons
  const iconProps = {
    size: 20,
    className: 'text-gray-500 mr-2',
  }
  // these are temporary test values to make sure the components work
  const vehicleItems = [
    {label: 'Personal Car (Toyota)', value: 'ABC1234'},
    {label: 'Business Car (Mazda)', value: 'XYZ1234'},
    {label: 'Random Car (Nissan)', value: 'LOL1234'},
  ];

  const typeItems = [
    {label: 'Business', value: 'business', category: 'builtin'},
    {label: 'Charity', value: 'charity', category: 'builtin'},
    {label: 'Military', value: 'military', category: 'builtin'},
    {label: 'Between Offices', value: 'between', category: 'custom'}

  ];

  const rateItems = [
    {label: 'IRS Standard Rate', value: 'irs', category: 'builtin'},
    {label: 'Company A Rate', value: 'companyA', category: 'category'}
  ];

  return (
    <SafeAreaView style={{flex: 1}}>
        <View style={{flex:1, padding: 20}}>
            
            <ScrollView className=''>
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
                icon={<FontAwesome name="car" {...iconProps} />}
              
              />

              <Dropdown 
                placeholder="Select type"
                items={typeItems}
                onValueChange={setType}
                value={type}
                icon={<FontAwesome name="list-ul" {...iconProps} />}
              
              />

              <Dropdown 
                placeholder="Select reimbursement rate"
                items={rateItems}
                onValueChange={setRate}
                value={rate}
                icon={<FontAwesome name="dollar" {...iconProps} />}
              />


            </ScrollView>
            
            
        </View>
    </SafeAreaView>

  )
}

export default Tracking
