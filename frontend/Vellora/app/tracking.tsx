import { View, Text } from 'react-native'
import React, { useState } from 'react'
// import MapView from 'react-native-maps';
import { useRouter } from 'expo-router';
import Mapbox from '@rnmapbox/maps';

// Import reusable components
import ScreenLayout from './components/ScreenLayout';
import TripDetailsForm from './components/TripDetailsForm';
import Button from './components/Button';
import { vehicleItems, typeItems, rateItems } from '../app/constants/dropdownOptions';
import UserLocationMap from './components/UserLocationMap';

const MAPBOX_KEY = process.env.EXPO_PUBLIC_API_KEY_MAPBOX_PUBLIC_ACCESS_TOKEN;
Mapbox.setAccessToken(`${MAPBOX_KEY}`);

const Tracking = () => {

  // state variables
  const [notes, setNotes] = useState('');
  const [vehicle, setVehicle] = useState<string | null>(null);
  const [type, setType] = useState<string | null>(null);
  const [rate, setRate] = useState<string | null>(null);
  const [parking, setParking] = useState<string>('');
  const [gas, setGas] = useState<string>('');

  // initialize router hook for navigation
  const router = useRouter();

  // start trip event handler. TO BE ADJUSTED
  const handleStartTrip = () => {

    // TRACKING START LOGIC TO BE IMPLEMENTED
    console.log('Starting trip...');
    router.push('/trackingInAction');

  };

  return (
    <ScreenLayout               // screen layout as the main wrapper
      footer={
        <Button 
          title='Start Trip'
          onPress={handleStartTrip}     // start the trip when footer button is pressed
          className=''                  // for additional styling
        />
      }

    >
      <Text className="text-3xl text-primaryPurple font-bold p-6">Live Track Current Trip</Text>

      {/* Temporary map display. TO BE CHANGED TO AN IMPLEMENTATION WITH CURRENT LOCATION VIA MAPBOX */}
      <View style={{ height: 300, width: '100%', borderRadius: 16, overflow: 'hidden' }}>
        <UserLocationMap />
      </View>

      {/* Container for displaying trip value and distance */}
      <View className='flex-row justify-between px-6 pt-6'>
        <Text className='text-xl'>
          Value: {' '}

          {/* Cost value. Starts at 0 */}
          <Text className='font-bold'>$0</Text>
        </Text>

        <Text className='text-xl'>
          Distance: {' '}

          {/* Distance value. Starts at 0 */}
          <Text className='font-bold'>0 mi</Text>
        </Text>
      </View>

      {/* display the form for trip details */}
      <TripDetailsForm 

        // state vairables
        notes={notes} setNotes={setNotes}
        vehicle={vehicle} setVehicle={setVehicle}
        type={type} setType={setType}
        rate={rate} setRate={setRate}
        parking={parking} setParking={setParking}
        gas={gas} setGas={setGas}

        // mock data arrays
        vehicleItems={vehicleItems}
        typeItems={typeItems}
        rateItems={rateItems}
      
      />
    </ScreenLayout>

  )
}

export default Tracking
