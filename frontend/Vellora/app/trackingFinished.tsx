import { View, Text } from 'react-native'
import React, { useState } from 'react'
import MapView from 'react-native-maps';
import { useRouter } from 'expo-router';

import ScreenLayout from './components/ScreenLayout';
import TripDetailsForm from './components/TripDetailsForm';
import EditableNumericDisplay from './components/EditableNumericDisplay';
import Button from './components/Button';

const TrackingFinished = () => {

  // state variables
  const [notes, setNotes] = useState('');
  const [vehicle, setVehicle] = useState<string | null>(null);
  const [type, setType] = useState<string | null>(null);
  const [rate, setRate] = useState<string | null>(null);
  const [parking, setParking] = useState<string>('0.00');
  const [tolls, setTolls] = useState<string>('0.00');
  const [gas, setGas] = useState<string>('0.00');
  const [tripValue, setTripValue] = useState('0.00');
  const [tripDistance, setTripDistance] = useState('0');
  const [startAddress, setStartAddress] = useState<string>('123 Start Street, Denton TX');
  const [endAddress, setEndAddress] = useState<string>('123 End Street, Denton TX');

  const router = useRouter();

  const handleSaveTrip = () => {
    console.log('Saving trip...');
    router.push('/(tabs)/history');
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
            <>
                <View className='flex-row justify-between mb-4'>
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
                    title='Save trip'
                    onPress={handleSaveTrip}
                    style={{top: 10}}
                />
            </>
        }
    >
        <MapView style={{width: '100%', height: 300}}/>
        <Text className='text-3xl text-primaryPurple font-bold pt-6 pl-6'>You arrived!</Text>
        <Text className='text-xl text-black p-6'>Make sure to update trip details:</Text>

        <TripDetailsForm 
            notes={notes} setNotes={setNotes}
            vehicle={vehicle} setVehicle={setVehicle}
            type={type} setType={setType}
            rate={rate} setRate={setRate}
            parking={parking} setParking={setParking}
            gas={gas} setGas={setGas}
            tolls={tolls} setTolls={setTolls}
            startAddress={startAddress} setStartAddress={setStartAddress}
            endAddress={endAddress} setEndAddress={setEndAddress}
            vehicleItems={vehicleItems}
            typeItems={typeItems}
            rateItems={rateItems}
            
        />

    </ScreenLayout>

  );
}

export default TrackingFinished;