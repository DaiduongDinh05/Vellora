// tracking.tsx (updated)
import { View, Text } from 'react-native'
import React, { useState, useEffect } from 'react'
import { useRouter } from 'expo-router';
import Mapbox from '@rnmapbox/maps';

// Import reusable components
import ScreenLayout from './components/ScreenLayout';
import TripDetailsForm from './components/TripDetailsForm';
import Button from './components/Button';
import { vehicleItems } from '../app/constants/dropdownOptions';
import UserLocationMap from './components/UserLocationMap';
import { useLocationTracking } from './hooks/useLocationTracking';
import { useRateOptions } from './hooks/useRateOptions';
import { useTripData } from './contexts/TripDataContext';

// service import
import { createTrip, getActiveTrip } from './services/Trips';

const MAPBOX_KEY = process.env.EXPO_PUBLIC_API_KEY_MAPBOX_PUBLIC_ACCESS_TOKEN;
Mapbox.setAccessToken(`${MAPBOX_KEY}`);

const Tracking = () => {
  // Use trip data context
  const { tripData, updateTripData, setTripId } = useTripData();
  
  // state variables
  const [notes, setNotes] = useState(tripData.notes);
  const [vehicle, setVehicle] = useState<string | null>(tripData.vehicle);
  const [type, setType] = useState<string | null>(tripData.type);
  const [rate, setRate] = useState<string | null>(tripData.rate);
  const [parking, setParking] = useState(tripData.parking);
  const [gas, setGas] = useState(tripData.gas);
  const [isStarting, setIsStarting] = useState(false);

  // initialize router hook for navigation
  const router = useRouter();

  // receive values from tracking logic
  const { startTracking, errorMessage, isTracking } = useLocationTracking();

  // fetch rates
  const { rateItems, categoryItems, loading, error, updateSelectedRate, selectedRate } = useRateOptions();

  // Update context when form data changes
  useEffect(() => {
    updateTripData({
      notes,
      vehicle,
      type,
      rate,
      parking,
      gas
    });
  }, [notes, vehicle, type, rate, parking, gas]);

  // handle rate selection
  const handleRateChange = (selectedRateId: string | null) => {
    setRate(selectedRateId);
    setType(null);      // reset category when rate changes
    updateSelectedRate(selectedRateId);
  };

  useEffect(() => {
    if (isTracking && isStarting) {
      router.push('/trackingInAction');
      setIsStarting(false);
    }
  }, [isTracking, isStarting]);

  // show loading state
  if (loading) {
    return (
        <Text className="text-3xl text-primaryPurple font-bold p-6">Loading rates...</Text>
      );
  }

  // Show error state
  if (error) {
    return (
      <>
        <Text className="text-3xl text-primaryPurple font-bold p-6">Error loading rates</Text>
        <Text className="text-red-500 p-6">{error}</Text>
        <Button 
          title="Retry" 
          onPress={() => window.location.reload()} 
        />
      </>
    );
  }

  // start trip event handler
  const handleStartTrip = async () => {
    // require input
    if (!vehicle || !type || !rate) {
      alert('Please fill in all required trip details');
      return;
    }

    console.log('STARTING...');
    setIsStarting(true);

    try {
      const activeTrip = await getActiveTrip();
      if (activeTrip) {
        alert('You already have an active trip. Please end it before starting a new one.');
        setIsStarting(false);
        return;
      }

      // PREPARE PAYLOAD FOR CREATETRIP API
      const tripPayload = {
        start_address: 'Current Location',
        purpose: notes || null,
        vehicle: vehicle || null,
        rate_customization_id: rate,
        rate_category_id: type
      };

      console.log('Creating trip with payload: ', tripPayload);

      const newTrip = await createTrip(tripPayload);
      console.log('trip create successfully: ', newTrip);

      // store the trip id in the context
      setTripId(newTrip.id);

      const success = await startTracking();

      // check if tracking start unsuccessfu;
      if(!success) {
        setIsStarting(false);
        alert(errorMessage || 'Failed to start tracking:(');
      }
    } catch (error) {
      console.log('Error creating trip: ', error);
      setIsStarting(false);
      alert('Failed to create trip. Please try again');
    }

  };

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

      <View style={{ height: 300, width: '100%', borderRadius: 16, overflow: 'hidden' }}>
        <UserLocationMap />
      </View>

      {/* Container for displaying trip value and distance */}
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

      {/* display the form for trip details */}
      <TripDetailsForm 
        // state variables
        notes={notes} setNotes={setNotes}
        vehicle={vehicle} setVehicle={setVehicle}
        type={type} setType={setType}
        rate={rate} setRate={handleRateChange}
        parking={parking} setParking={setParking}
        gas={gas} setGas={setGas}

        // mock data arrays
        vehicleItems={vehicleItems}
        typeItems={categoryItems}
        rateItems={rateItems}
      />
    </ScreenLayout>
  )
}

export default Tracking