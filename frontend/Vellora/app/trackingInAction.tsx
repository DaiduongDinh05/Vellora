import { Image, Text, View } from 'react-native'
import React, { useState } from 'react'
import { useRouter } from 'expo-router';
import ScreenLayout from './components/ScreenLayout';
import NoteInput from './components/NoteInput';
import CurrencyInput from './components/CurrencyInput';
import Button from './components/Button';

const trackingInAction = () => {
    // state variables
    const [notes, setNotes] = useState('');
    const [parking, setParking] = useState<string>('');
    const [gas, setGas] = useState<string>('');
    const router = useRouter();

    // end trip event handler. TO BE ADJUSTED
    const handleEndTrip = () => {

        // TRACKING END LOGIC TO BE IMPLEMENTED
        console.log('Starting trip...');
        router.push('/trackingFinished');

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
                        <Text className='font-bold'>0 mi</Text>
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

export default trackingInAction
