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

const MAPBOX_KEY = process.env.EXPO_PUBLIC_API_KEY_MAPBOX_PUBLIC_ACCESS_TOKEN;

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
  const [startAddress, setStartAddress] = useState<string>('Loading address...');
  const [endAddress, setEndAddress] = useState<string>('Loading address...');
  const [tripGeometry, setTripGeometry] = useState<object | null>(null);
  const[isLoadingAddresses, setIsLoadingAddresses] = useState(false);

  // get trip data from navigation params
  const params = useLocalSearchParams();
  const routeDistance = params.distance as string;
  const routeGeometry = params.geometry as string;

  // initialize router hook for navigation
  const router = useRouter();

  // convert coordinates to address using mapbox
  const findGeocode = async (longitude: number, latitude: number): Promise<string> => {
    try {

        // call mapbox geocoding api
        const response = await fetch(
            `https://api.mapbox.com/geocoding/v5/mapbox.places/${longitude},${latitude}.json?access_token=${MAPBOX_KEY}`
        );

        // handle errors from api
        if (!response.ok) {
            throw new Error(`Geocoding failed: ${response.status}`);
        }

        // parse response
        const data = await response.json();

        // extract address
        if (data.features && data.features.length > 0) {
            return data.features[0].place_name;             // return address
        } else {
            return 'Address not found';
        }
    } catch (error) {
        console.error('Error geocoding: ', error);
        return 'Unable to get address';
    }
  };

  // extract start and end coordinates from the geometry and convert them to addresses
  const getAddressFromGeometry = async (geometry: any) => {

    // check geometry validity
    if (!geometry || !geometry.coordinates || !Array.isArray(geometry.coordinates)) {
        console.log('No valid geometry found');
        return;
    }

    setIsLoadingAddresses(true);

    try {
        const coordinates = geometry.coordinates;

        // process coordinates if available
        if (coordinates.length > 0) {

            // get start address from first coordinate in the route
            const startPoint = coordinates[0];
            const startAddress = await findGeocode(startPoint[0], startPoint[1]);
            setStartAddress(startAddress);

            // get end address from last coordinate in the route
            const endPoint = coordinates[coordinates.length - 1];
            const endAddress = await findGeocode(endPoint[0], endPoint[1]);
            setEndAddress(endAddress);

            // debugging
            console.log('Start address: ', startAddress);
            console.log('End address: ', endAddress);
        }
    } catch (error) {
        console.error('Error updating addresses: ', error);
        setStartAddress('Error loading address');
        setEndAddress('Error loading address');
    } finally {
        setIsLoadingAddresses(false);
    }
  };

  // parse route geometry qhen component mounts or geometry changes
  useEffect(() => {
    if (routeGeometry) {
        try {
            const parsedGeometry = JSON.parse(routeGeometry);
            setTripGeometry(parsedGeometry);
            console.log('Parsed trip geometry: ', parsedGeometry);

            // start address lookup
            getAddressFromGeometry(parsedGeometry);
        } catch (error) {
            console.error('Error parsing geometry: ', error);
        }
    }
  }, [routeGeometry]);

  // set distance from route parameters
  useEffect(() => {
    if (routeDistance) {
        setTripDistance(routeDistance);
    }
  }, [routeDistance]);
  
  // calculate trip value when rate or distance changes
  useEffect(() => {
    if (rate && tripDistance) {
        let rateValue = parseFloat(rate.replace('$', ''));
        let distanceValue = parseFloat(tripDistance);
        const calculatedValue = (rateValue * distanceValue).toFixed(2);
        setTripValue(calculatedValue);
    }
  }, [rate, tripDistance]);

  // end end trip event handler
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
            <GeometryMap geometry={tripGeometry}/> 

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