import { View, Text } from 'react-native'
import React, { useState, useEffect } from 'react'
import { useRouter, useLocalSearchParams } from 'expo-router';

// Import reusable components
import ScreenLayout from './components/ScreenLayout';
import TripDetailsForm from './components/TripDetailsForm';
import EditableNumericDisplay from './components/EditableNumericDisplay';
import Button from './components/Button';
import { vehicleItems, typeItems, rateItems } from '../app/constants/dropdownOptions';
import GeometryMap from './components/GeometryMap';
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
  const [tripGeometry, setTripGeometry] = useState<object | null>(null);

  // get trip data from navigation params
  const params = useLocalSearchParams();
  const routeDistance = params.distance as string;
  const routeGeometry = params.geometry as string;

  // initialize router hook for navigation
  const router = useRouter();

  useEffect(() => {
    if (routeGeometry) {
        try {
            const parsedGeometry = JSON.parse(routeGeometry);
            setTripGeometry(parsedGeometry);
            console.log('Parsed trip geometry: ', parsedGeometry);
        } catch (error) {
            console.error('Error parsing geometry: ', error);
        }
    }
  }, [routeGeometry]);

  useEffect(() => {
    if (routeDistance) {
        setTripDistance(routeDistance);
    }
  }, [routeDistance]);

  useEffect(() => {
    if (rate && tripDistance) {
        let rateValue = parseFloat(rate.replace('$', ''));
        let distanceValue = parseFloat(tripDistance);
        const calculatedValue = (rateValue * distanceValue).toFixed(2);
        setTripValue(calculatedValue);
    }
  }, [rate, tripDistance]);

  // end end trip event handler. TO BE ADJUSTED
  const handleSaveTrip = () => {
    console.log('Saving trip...');
    router.push('/(tabs)/history');
  };


  return (
    <ScreenLayout       // screen layout as the main wrapper

        // return calculated value and distance with an option for user to edit them
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
        {/* GEOMETRY PATH */}
        <View style={{ height: 300, width: '100%', borderRadius: 16, overflow: 'hidden' }}>
            <GeometryMap /> 

        </View>
        <Text className='text-3xl text-primaryPurple font-bold pt-6 pl-6'>You arrived!</Text>
        <Text className='text-xl text-black p-6'>Make sure to update trip details:</Text>

        <TripDetailsForm 

            // state variables
            notes={notes} setNotes={setNotes}
            vehicle={vehicle} setVehicle={setVehicle}
            type={type} setType={setType}
            rate={rate} setRate={setRate}
            parking={parking} setParking={setParking}
            gas={gas} setGas={setGas}
            tolls={tolls} setTolls={setTolls}
            startAddress={startAddress} setStartAddress={setStartAddress}
            endAddress={endAddress} setEndAddress={setEndAddress}

            // mock data arrays
            vehicleItems={vehicleItems}
            typeItems={typeItems}
            rateItems={rateItems}
            
        />

    </ScreenLayout>

  );
}

export default TrackingFinished;