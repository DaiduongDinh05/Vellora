import { Image, StyleSheet, Text, View, TouchableWithoutFeedback, Keyboard } from 'react-native'
import React, { useState } from 'react'
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import NoteInput from './components/NoteInput';
import CurrencyInput from './components/CurrencyInput';
import Button from './components/Button';
import { useRouter } from 'expo-router';

const trackingInAction = () => {
    // state variables
    const [notes, setNotes] = useState('');
    const [parking, setParking] = useState<string>('');
    const [gas, setGas] = useState<string>('');
    const router = useRouter();
    const insets = useSafeAreaInsets();

    const handleEndTrip = () => {
        console.log('Starting trip...');
        router.push('/trackingFinished');

    };
    
    return (
        <TouchableWithoutFeedback onPress={() => Keyboard.dismiss()} accessible={false}>
            <View style={{flex: 1, backgroundColor: '#fff'}}>
                <View style={{paddingTop: insets.top}} />

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

                <View className='bg-white px-6 pt-4 border border-gray-300' style={{position: 'absolute', bottom: 0, padding: 30, paddingTop: 20, width: '100%'}}>
                    <Button 
                        title="End Trip"
                        onPress={handleEndTrip}
                        className=""
                    />
        
                </View>
            </View>
        </TouchableWithoutFeedback>
    
    )
}

export default trackingInAction

const styles = StyleSheet.create({})