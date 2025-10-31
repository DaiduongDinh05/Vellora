import { View, Text, StyleSheet, TouchableWithoutFeedback, Keyboard } from 'react-native'
import React, { useState } from 'react'
import { SafeAreaView, useSafeAreaInsets } from 'react-native-safe-area-context';
import NoteInput from './components/NoteInput'
import Dropdown from './components/Dropdown'
import { ScrollView } from 'react-native';
import { FontAwesome } from '@expo/vector-icons';
import CurrencyInput from './components/CurrencyInput';
import Button from './components/Button';
import MapView from 'react-native-maps';
import { useRouter } from 'expo-router';
import FilledAddressBox from './components/FilledAddressBox';
import EditableNumericDisplay from './components/EditableNumericDisplay';

const TrackingFinished = () => {

  // state variables
  const [notes, setNotes] = useState('');
  const [vehicle, setVehicle] = useState<string | null>(null);
  const [type, setType] = useState<string | null>(null);
  const [rate, setRate] = useState<string | null>(null);
  const [parking, setParking] = useState<string>('0.00');
  const [gas, setGas] = useState<string>('0.00');
  const [tripValue, setTripValue] = useState('0.00');
  const [tripDistance, setTripDistance] = useState('0');
  const [startAddress, setStartAddress] = useState<string>('123 Start Street, Denton TX');
  const [endAddress, setEndAddress] = useState<string>('123 End Street, Denton TX');

  const router = useRouter();
  const insets = useSafeAreaInsets();

  const handleStartTrip = () => {
    console.log('Starting trip...');
    router.push('/(tabs)/history');
  };

  // common style for icons
  const iconProps = {
    size: 18,
  };
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
    <TouchableWithoutFeedback onPress={() => Keyboard.dismiss()} accessible={false}>

      <View style={{flex: 1, backgroundColor: '#fff'}}>
        <ScrollView style={{flex: 1}} 
          contentContainerStyle={{ paddingBottom: 120 }}
          indicatorStyle='black' 
          persistentScrollbar={true}>
          
          <MapView style={{width: '100%', height: 300}}/>
          <Text className="text-3xl text-primaryPurple font-bold pt-6 pl-6">You arrived!</Text>
          <Text className="text-xl text-black p-6">Make sure to update trip details:</Text>
            {/* create a scrollable form and add gaps between child components */}
            <View style={{padding: 25, gap: 16}}>

                {/* render notes input */}
                <FilledAddressBox 
                    value={startAddress}
                    onChangeText={setStartAddress}
                
                />
                <FilledAddressBox 
                    value={endAddress}
                    onChangeText={setEndAddress}
                />

                <View className='flex-row gap-4'>
                  <CurrencyInput 
                    label='Parking'
                    value={parking}
                    onChangeText={setParking}
                    className="flex-1"
                  />
                  <CurrencyInput 
                    label='Tolls'
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

            </View>    
                
        </ScrollView>
        <View className='bg-white px-6 pt-4 border border-gray-300' style={{position: 'absolute', bottom: 0, padding: 30, paddingTop: 20, width: '100%'}}>
          
            <View className='flex-row justify-between'>
                <EditableNumericDisplay
                    label='Value'
                    value={tripValue}
                    onChangeText={setTripValue}
                    unit='$'
                />
                <EditableNumericDisplay
                    label='Distance'
                    value={tripDistance}
                    onChangeText={setTripDistance}
                    unit='mi'
                />
                 
            </View>
            <Button 
                title="End Trip"
                onPress={handleStartTrip}
                className="top-4"
            />

        </View>

      </View>
    </TouchableWithoutFeedback>

  )
}

export default TrackingFinished;