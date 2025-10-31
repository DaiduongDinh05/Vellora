import { View, Text } from 'react-native'
import React, { useState } from 'react'
import MapView from 'react-native-maps';
import { useRouter } from 'expo-router';

// Import reusable components
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

  // initialize router hook for navigation
  const router = useRouter();

  // start trip event handler. TO BE ADJUSTED
  const handleStartTrip = () => {

    // TRACKING START LOGIC TO BE IMPLEMENTED
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
      <MapView style={{width: '100%', height: 300}}/>

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
