import { Image, Text, View } from 'react-native'
import React, { useState, useEffect } from 'react'
import { useRouter } from 'expo-router';
import ScreenLayout from './components/ScreenLayout';
import NoteInput from './components/NoteInput';
import CurrencyInput from './components/CurrencyInput';
import Button from './components/Button';
import { useLocationTracking } from './hooks/useLocationTracking';

const TrackingInAction = () => {
    // state variables
    const [notes, setNotes] = useState('');
    const [parking, setParking] = useState<string>('');
    const [gas, setGas] = useState<string>('');
    const [isStopping, setIsStopping] = useState(false);
    const [displayDistance, setDisplayDistance] = useState(0);

    const router = useRouter();

    const { stopTracking, isTracking, totalTripDistance, errorMessage } = useLocationTracking();

    useEffect(() => {
        const miles = (totalTripDistance / 1609.34).toFixed(2);
        setDisplayDistance(parseFloat(miles));
    }, [totalTripDistance]);


    // end trip event handler. TO BE ADJUSTED
    const handleEndTrip = async () => {

        // TRACKING END LOGIC TO BE IMPLEMENTED
        console.log('ENDING');
        setIsStopping(true);
        
        const tripData = await stopTracking();

        if (tripData.distance > 0) {
            const miles = (tripData.distance / 1609.34).toFixed(2);

            router.push({
                pathname: '/trackingFinished',
                params: {
                    distance: miles,
                    geometry: JSON.stringify(tripData.geometry)
                }
            });
        } else{
            router.push({
                pathname: '/trackingFinished',
                params: {
                    distance: '0',
                    geometry:''
                }
            });
        }
        setIsStopping(false);

    };
    
    return (
        <ScreenLayout       // screen layout as the main wrapper
            footer={
                <Button 
                    title='End Trip'
                    onPress={handleEndTrip}     // end the trip when footer button is pressed
                    className=''                // for additional styling
                />
            }
        >

            <Text className="text-3xl text-primaryPurple font-bold p-6">Live tracking your trip...</Text>


            {/* TEST: show tracking activity */}
            <View className='px-6 pb-4'>
                {isTracking ? (
                    <Text className='text-green-500 text-center text-lg font-semibold'>tracking active</Text>
                ) : (
                    <Text className='text-green-500 text-center text-lg font-semibold'>tracking INACTIVE</Text>

                )}

            </View>
            {/* Display the car gif */}
            <View style={{justifyContent: 'center', alignItems: 'center'}}>
                <Image source={require('./assets/car.gif')} style={{width: 200, height: 200}}/>
            </View>

            <Text className="text-3xl text-black font-bold p-6 text-center w-full">Have a safe trip!</Text>

            <View style={{padding: 25, gap: 16}}>

                {/* Container for displaying unadjustable live trip values and distance */}
                <View className='flex-row justify-between'>
                    <Text className='text-xl'>
                        Value: {' '}

                        {/* Cost value. TO BE CHANGED TO REAL TIME COLLECTED AMOUNT */}
                        <Text className='font-bold'>$0</Text>
                    </Text>
                    <Text className='text-xl'>
                        Distance: {' '}

                        {/* Distance value. TO BE CHANGED TO REAL TIME COLLECTED AMOUNT */}
                        <Text className='font-bold'>{displayDistance} mi</Text>
                    </Text>
                </View>

                {/* render notes input */}
                <NoteInput 
                    placeholder="Add your crazy notes"
                    value={notes}
                    onChangeText={setNotes}
                    className=''
                />

                {/* Render input boxes for currency types */}
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


            </View>    

        </ScreenLayout>

    );
}

export default TrackingInAction
