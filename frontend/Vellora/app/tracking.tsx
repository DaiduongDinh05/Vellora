import { View, Text } from 'react-native'
import React, { useState } from 'react'
import MapView from 'react-native-maps';
import { useRouter } from 'expo-router';

import ScreenLayout from './components/ScreenLayout';
import TripDetailsForm from './components/TripDetailsForm';
import Button from './components/Button';

const Tracking = () => {

  // state variables
  const [notes, setNotes] = useState('');
  const [vehicle, setVehicle] = useState<string | null>(null);
  const [type, setType] = useState<string | null>(null);
  const [rate, setRate] = useState<string | null>(null);
  const [parking, setParking] = useState<string>('');
  const [gas, setGas] = useState<string>('');

  const router = useRouter();

  const handleStartTrip = () => {
    console.log('Starting trip...');
    router.push('/trackingInAction');
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

    <ScreenLayout
      footer={
        <Button 
          title='Start Trip'
          onPress={handleStartTrip}
          className=''
        />
      }

    >
      <Text className="text-3xl text-primaryPurple font-bold p-6">Live Track Current Trip</Text>
      <MapView style={{width: '100%', height: 300}}/>
      {/* create a scrollable form and add gaps between child components */}
      <View className='flex-row justify-between px-6 pt-6'>
        <Text className='text-xl'>
          Value: {' '}
          <Text className='font-bold'>$0</Text>
        </Text>
        <Text className='text-xl'>
          Distance: {' '}
          <Text className='font-bold'>0 mi</Text>
        </Text>
      </View>

      <TripDetailsForm 
        notes={notes} setNotes={setNotes}
        vehicle={vehicle} setVehicle={setVehicle}
        type={type} setType={setType}
        rate={rate} setRate={setRate}
        parking={parking} setParking={setParking}
        gas={gas} setGas={setGas}
        vehicleItems={vehicleItems}
        typeItems={typeItems}
        rateItems={rateItems}
      
      />
    </ScreenLayout>

  )
}

export default Tracking
