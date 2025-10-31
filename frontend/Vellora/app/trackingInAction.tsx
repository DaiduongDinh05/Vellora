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

    const handleEndTrip = () => {
        console.log('Starting trip...');
        router.push('/trackingFinished');

    };
    
    return (
        <ScreenLayout
            footer={
                <Button 
                    title='End Trip'
                    onPress={handleEndTrip}
                    className=''
                />
            }
        >

            <Text className="text-3xl text-primaryPurple font-bold p-6">Live tracking your trip...</Text>

            <View style={{justifyContent: 'center', alignItems: 'center'}}>
                <Image source={require('./assets/car.gif')} style={{width: 200, height: 200}}/>
            </View>
            <Text className="text-3xl text-black font-bold p-6 text-center w-full">Have a safe trip!</Text>

            {/* create a scrollable form and add gaps between child components */}
            <View style={{padding: 25, gap: 16}}>
                <View className='flex-row justify-between'>
                    <Text className='text-xl'>
                        Value: {' '}
                        <Text className='font-bold'>$0</Text>
                    </Text>
                    <Text className='text-xl'>
                        Distance: {' '}
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
