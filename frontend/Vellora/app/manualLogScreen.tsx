import { Text, View, TouchableOpacity, Platform } from 'react-native'
import React, { useState, useEffect } from 'react'
import { useRouter } from 'expo-router';
import { FontAwesome } from '@expo/vector-icons';
import DateTimePicker, { DateTimePickerEvent } from '@react-native-community/datetimepicker';
import { DateTimePickerAndroid } from '@react-native-community/datetimepicker';

// component and data imports
import { vehicleItems } from '../app/constants/dropdownOptions';
import ScreenLayout from './components/ScreenLayout';
import TripDetailsForm from './components/TripDetailsForm';
import Button from './components/Button';
import EditableNumericDisplay from './components/EditableNumericDisplay';
import { useRateOptions } from './hooks/useRateOptions';
import { useTripData } from './contexts/TripDataContext';

const ManualLogScreen = () => {

    // use trip data context
    const { tripData, updateTripData, resetTripData } = useTripData();

    // use rate options hook for dynamic rates
    const { rateItems, categoryItems, loading, error, updateSelectedRate } = useRateOptions();

    // state variables
    const [startDate, setStartDate] = useState(new Date());
    const [endDate, setEndDate] = useState(new Date());
    // const [showStartPicker, setShowStartPicker] = useState(false);
    // const [showEndPicker, setShowEndPicker] = useState(false);

    const [showStartIOS, setShowStartIOS] = useState(false);
    const [showEndIOS, setShowEndIOS] = useState(false);

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

    // handle rate selection to update categories
    const handleRateChange = (selectedRateId: string | null) => {
        setRate(selectedRateId);
        setType(null); // reset category when rate changes
        updateSelectedRate(selectedRateId);
    };

    // calculate trip value when rate or distance changes
    useEffect(() => {
        if (rate && tripDistance) {
            // extract the actual numeric value from rateItems
            const selectedRateItem = rateItems.find(item => item.value === rate);
            if (selectedRateItem && selectedRateItem.originalRate) {

                // find the selected category's cost per mile
                const selectedCategory = categoryItems.find(item => item.value === type);

                if (selectedCategory && selectedCategory.originalCategory) {

                    const rateValue = selectedCategory.originalCategory.cost_per_mile;
                    let distanceValue = parseFloat(tripDistance);
                    const calculatedValue = (rateValue * distanceValue).toFixed(2);
                    setTripValue(calculatedValue);

                }
            }
        }
    }, [rate, type, tripDistance, rateItems, categoryItems]);

    // // when a user select a start date or closes the picker, hide it
    // const onStartDateChange = (event: DateTimePickerEvent, selectedDate?: Date) => {

    //     //  if the user dismissed (cancelled) the picker, hide it
    //     if (event.type === 'dismissed') {
    //         setShowStartPicker(false);
    //         return;
    //     }

    //     // if the user set a date/time
    //     if (event.type === 'set' && selectedDate) {
    //         setShowStartPicker(false);
    //         setStartDate(selectedDate);
    //     }

    // };

    // // when a user select an end date or closes the picker, hide it
    // const onEndDateChange = (event: DateTimePickerEvent, selectedDate?: Date) => {

    //     // if the user dismissed (cancelled) the picker, hide it
    //     if (event.type === 'dismissed') {
    //         setShowEndPicker(false);
    //         return;
    //     }

    //     // if the user set a date/time
    //     if (event.type === 'set' && selectedDate) {
    //         setShowEndPicker(false);
    //         setEndDate(selectedDate);
    //     }
    // };


    // toggle functions for the date pickers
    // const toggleStartPicker = () => {
    //     setShowStartPicker(prev => !prev);
    // };

    // const toggleEndPicker = () => {
    //     setShowEndPicker(prev => !prev);
    // };

    // OPEN ANDROID PICKER
    const openAndroidDateTimePicker = (
        currentDate: Date,
        onChange: (event: DateTimePickerEvent, date?: Date) => void
        ) => {
        DateTimePickerAndroid.open({
            value: currentDate,
            onChange: (event, date) => {
            if (date) {
                // first pick date
                DateTimePickerAndroid.open({
                value: date,
                mode: 'time',
                onChange, // final combined result
                });
            }
            },
            mode: 'date',
        });
    };

    // HANDLER TO OPEN START PICKER
    const handleStartPress = () => {
        if (Platform.OS === 'ios') {
            setShowStartIOS(!showStartIOS);
        } else {
            openAndroidDateTimePicker(startDate, (event, selectedDate) => {
                if (event.type === "set" && selectedDate) {
                    setStartDate(selectedDate);
                }
            });
        }
    };

    // HANDLER TO OPEN END PICKER
    const handleEndPress = () => {
        if (Platform.OS === 'ios') {
            setShowEndIOS(!showEndIOS);
        } else {
             openAndroidDateTimePicker(startDate, (event, selectedDate) => {
                if (event.type === "set" && selectedDate) {
                    setEndDate(selectedDate);
                }
            });
        }
    };

    // add trip to history event handler. TO BE ADJUSTED
    const handleAddTrip = () => {
        console.log("Adding trip to history...");

        // manually logged trip data object
        const manualTripData = {
            notes,
            vehicle,
            type,
            rate,
            parking,
            gas,
            tolls,
            startAddress,
            endAddress,
            distance: tripDistance,
            value: tripValue,
            startTime: startDate.toISOString(),
            endTime: endDate.toISOString(),
            isManual: true,                         // flag to identify manual trips
            timestamp: new Date().toISOString()
        };

        console.log('Manual trip data to save:', manualTripData);

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
                <TouchableOpacity onPress={handleStartPress}>
                    {/* style it to look like a dropdown to match the general visuals */}
                    <View className='flex-row border items-center border-gray-300 bg-white rounded-lg px-3 py-3'>
                        <View className='w-6 items-center'>
                            <FontAwesome name='calendar' {...iconProps} />
                        </View>
                        <Text style={{fontSize: 16, color: 'black', marginLeft: 10}}>
                            {startDate.toLocaleString()}
                        </Text>

                    </View>

                </TouchableOpacity>

                {/* iOS inline picker */}
                {Platform.OS === 'ios' && showStartIOS && (
                    <DateTimePicker
                        value={startDate}
                        mode='datetime'
                        display='spinner'
                        onChange={(event, date) => date && setStartDate(date)}
                    />
                )}

                <Text className='text-sm text-gray-500 mb-1'>End Time</Text>
                {/* button for picking a date and time */}
                <TouchableOpacity onPress={handleEndPress}>
                    {/* style it to look like a dropdown to match the general visuals */}
                    <View className='flex-row border items-center border-gray-300 bg-white rounded-lg px-3 py-3'>
                        <View className='w-6 items-center'>
                            <FontAwesome name='calendar' {...iconProps} />
                        </View>
                        <Text style={{fontSize: 16, color: 'black', marginLeft: 10}}>
                            {endDate.toLocaleString()}
                        </Text>

                    </View>

                </TouchableOpacity>

                {/* picker where you choose date and time. Hidden until showpicker is set true*/}
                {/* iOS inline picker */}
                {Platform.OS === 'ios' && showEndIOS && (
                    <DateTimePicker
                        value={endDate}
                        mode='datetime'
                        display='spinner'
                        onChange={(event, date) => date && setEndDate(date)}
                    />
                )}
            </View>
                <TripDetailsForm 

                    // state variables
                    notes={notes} setNotes={setNotes}
                    vehicle={vehicle} setVehicle={setVehicle}
                    type={type} setType={setType}
                    rate={rate} setRate={handleRateChange}
                    parking={parking} setParking={setParking}
                    gas={gas} setGas={setGas}
                    tolls={tolls} setTolls={setTolls}
                    startAddress={startAddress} setStartAddress={setStartAddress}
                    endAddress={endAddress} setEndAddress={setEndAddress}

                    // mock data arrays
                    vehicleItems={vehicleItems}
                    typeItems={categoryItems}
                    rateItems={rateItems}
                    
                />


            


        </ScreenLayout>
    )
}

export default ManualLogScreen
