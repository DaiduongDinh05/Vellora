import { View } from 'react-native'
import React, { useState } from 'react'
import { SafeAreaView } from 'react-native-safe-area-context';
import NoteInput from './components/NoteInput'
import Dropdown from './components/Dropdown'
import { ScrollView } from 'react-native';
import { FontAwesome } from '@expo/vector-icons';
import CurrencyInput from './components/CurrencyInput';

const Tracking = () => {

  // state variables
  const [notes, setNotes] = useState('');
  const [vehicle, setVehicle] = useState<string | null>(null);
  const [type, setType] = useState<string | null>(null);
  const [rate, setRate] = useState<string | null>(null);
  const [parking, setParking] = useState<string>('');
  const [gas, setGas] = useState<string>('');


  // common style for icons
  const iconProps = {
    size: 18,
  }
  // these are temporary test values to make sure the components work
  // vehicle options
  const vehicleItems = [
    {label: 'Personal Car (Toyota)', value: 'ABC1234'},
    {label: 'Business Car (Mazda)', value: 'XYZ1234'},
    {label: 'Random Car (Nissan)', value: 'LOL1234'},
  ];

  // type options
  const typeItems = [
    {label: 'Business', value: 'business', category: 'builtin'},
    {label: 'Charity', value: 'charity', category: 'builtin'},
    {label: 'Military', value: 'military', category: 'builtin'},
    {label: 'Between Offices', value: 'between', category: 'custom'}

  ];

  // reimbursement rate options
  const rateItems = [
    {label: 'IRS Standard Rate', value: 'irs', category: 'builtin'},
    {label: 'Company A Rate', value: 'companyA', category: 'category'}
  ];

  return (
    <SafeAreaView style={{flex: 1}}>
        <View style={{flex:1, padding: 20}}>

            {/* create a scrollable form and add gaps between child components */}
            <ScrollView contentContainerStyle={{rowGap: 16}}>

              {/* render notes input */}
              <NoteInput 
                placeholder="Add your crazy notes"
                value={notes}
                onChangeText={setNotes}
                className=''
              />

              <View className='flex-row gap-4'>
                <CurrencyInput 
                  label='Parking'
                  value={parking}
                  onChangeText={setParking}
                  className="flex-1"
                />

                <CurrencyInput 
                  label='Gas'
                  value={gas}
                  onChangeText={setGas}
                  className="flex-1"
                />
              </View>

              {/* render vehicle dropdown */}
              <Dropdown 
                placeholder="Select vehicle"
                items={vehicleItems}
                onValueChange={setVehicle}
                value={vehicle}
                icon={<FontAwesome name="car" {...iconProps} />}
              />

              {/* render type dropdown */}
              <Dropdown 
                placeholder="Select type"
                items={typeItems}
                onValueChange={setType}
                value={type}
                icon={<FontAwesome name="list-ul" {...iconProps} />}
              />

              {/* render rate dropdown */}
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
