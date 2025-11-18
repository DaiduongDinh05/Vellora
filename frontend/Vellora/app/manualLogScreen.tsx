import { Text, View, TouchableOpacity } from 'react-native'
import React, { useState } from 'react'
import { useRouter } from 'expo-router';
import { FontAwesome } from '@expo/vector-icons';
import DateTimePicker, { DateTimePickerEvent } from '@react-native-community/datetimepicker';

// component and data imports
import { vehicleItems, typeItems, rateItems } from '../app/constants/dropdownOptions';
import ScreenLayout from './components/ScreenLayout';
import TripDetailsForm from './components/TripDetailsForm';
import Button from './components/Button';
import EditableNumericDisplay from './components/EditableNumericDisplay';

const ManualLogScreen = () => {

    // state variables
    const [date, setDate] = useState(new Date());
    const [showPicker, setShowPicker] = useState(false);
    const [startAddress, setStartAddress] = useState('');
    const [endAddress, setEndAddress] = useState('');
    const [notes, setNotes] = useState('');
    const [vehicle, setVehicle] = useState<string | null>(null);
    const [type, setType] = useState<string | null>(null);
    const [rate, setRate] = useState<string | null>(null);
    const [parking, setParking] = useState<string>('');
    const [gas, setGas] = useState<string>('');
    const [tolls, setTolls] = useState('0.00');

    // sticky footer state variables
    const [tripValue, setTripValue] = useState('0.00');
    const [tripDistance, setTripDistance] = useState('0');
    
    const router = useRouter();

    // when a user select a date or closes the picker, hide it
    const onDateChange = (event: DateTimePickerEvent, selectedDate?: Date) => {
        setShowPicker(false);
        if(selectedDate){
            setDate(selectedDate);
        }
    };

    // add trip to history event handler. TO BE ADJUSTED
    const handleAddTrip = () => {
        console.log("Adding trip to history...");
        router.push('/(tabs)/history');
    };


    // icons style object
    const iconProps = { size: 18 };


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
                        onPress={handleAddTrip}
                        style={{top: 10}}
                    />
                </>
            }
        >
            <Text className='text-3xl text-primaryPurple font-bold p-6'>Manually Log Trip</Text>


            <View style={{ paddingHorizontal: 25, gap: 16 }}>

                <Text className='text-sm text-gray-500 mb-1'>Start Time</Text>
                {/* button for picking a date and time */}
                <TouchableOpacity onPress={() => setShowPicker(true)}>
                    {/* style it to look like a dropdown to match the general visuals */}
                    <View className='flex-row border items-center border-gray-300 bg-white rounded-lg px-3 py-3'>
                        <View className='w-6 items-center'>
                            <FontAwesome name='calendar' {...iconProps} />
                        </View>
                        <Text style={{fontSize: 16, color: 'black', marginLeft: 10}}>
                            {date.toLocaleString()}
                        </Text>

                    </View>

                </TouchableOpacity>

                {/* picker where you choose date and time. Hidden until showpicker is set true*/}
                {
                    showPicker && (
                        <DateTimePicker
                            value={date}
                            mode='datetime'
                            display='default'
                            onChange={onDateChange}
                        />
                    )
                }

                <Text className='text-sm text-gray-500 mb-1'>End Time</Text>
                {/* button for picking a date and time */}
                <TouchableOpacity onPress={() => setShowPicker(true)}>
                    {/* style it to look like a dropdown to match the general visuals */}
                    <View className='flex-row border items-center border-gray-300 bg-white rounded-lg px-3 py-3'>
                        <View className='w-6 items-center'>
                            <FontAwesome name='calendar' {...iconProps} />
                        </View>
                        <Text style={{fontSize: 16, color: 'black', marginLeft: 10}}>
                            {date.toLocaleString()}
                        </Text>

                    </View>

                </TouchableOpacity>

                {/* picker where you choose date and time. Hidden until showpicker is set true*/}
                {
                    showPicker && (
                        <DateTimePicker
                            value={date}
                            mode='datetime'
                            display='default'
                            onChange={onDateChange}
                        />
                    )
                }
            </View>
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
    )
}

export default ManualLogScreen
