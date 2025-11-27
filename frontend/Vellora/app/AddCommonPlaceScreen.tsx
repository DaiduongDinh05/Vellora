import { Text, View } from 'react-native'
import React, { useEffect, useState } from 'react'
import Mapbox from '@rnmapbox/maps';
import { useRouter } from 'expo-router';
import * as Location from 'expo-location';
import { Keyboard, TouchableOpacity, TextInput } from 'react-native';
import { FontAwesome } from '@expo/vector-icons';

import ScreenLayout from './components/ScreenLayout';
import AddressInput from './components/AddressInput';
import Button from './components/Button';

const MAPBOX_TOKEN = process.env.EXPO_PUBLIC_API_KEY_MAPBOX_PUBLIC_ACCESS_TOKEN;
Mapbox.setAccessToken(`${MAPBOX_TOKEN}`);

const AddCommonPlaceScreen = () => {
    const router = useRouter();

    const [name, setName] = useState('');
    const [address, setAddress] = useState('');
    const [coordinates, setCoordinates] = useState<[number, number] | null>(null);

    // initial location logic
    // make the map show user's current location if they didn't type an address yet
    
    useEffect(() => {
        (async () => {
            try{
                let { status } = await Location.requestForegroundPermissionsAsync();
                if (status !== 'granted') {
                    console.log('Permission denied');
                    return;
                }
                let loc = await Location.getCurrentPositionAsync({
                    accuracy: Location.Accuracy.Balanced,
    
                });
    
                // update state only if we haven't selected an address yet
                if (!coordinates) {
                    setCoordinates([loc.coords.longitude, loc.coords.latitude]);
                }
            } catch (error) {
                console.error('Error getting location: ', error);
            }
            
        })();
    }, []);

    const handleAddressSelect = (addressData: any) => {
        if (addressData && addressData.center) {
            setAddress(addressData.place_name);
            setCoordinates(addressData.center);
            Keyboard.dismiss(); 
        }
    };

    const handleSavePlace = () => {
        
        if (!name || !address || !coordinates) {
            alert('Please provide all details');
            return;
        }

        // prepare data payload
        const placePayload = {
            title: name,
            address: address,
            geometry: {
                type: 'Point',
                coordinates: coordinates
            },
        };

        console.log('Saving common place: ', placePayload);

        try {
            // logic to save the common place
            // change to backend API later

            router.back();
        } catch (error) {
            console.error('Error saving common place: ', error);
            alert('Failed to save the place. Please try again.');
        }
    };


    return (
        <ScreenLayout
            footer={
                <Button 
                    title="Save Place"
                    onPress={handleSavePlace}
                    className='py-4 px-5'
                />
            }
        >
            <View className='px-6 pt-4 flex-row items-center justify-between'>

                <TouchableOpacity
                    onPress={() => router.back()}
                    className='bg-gray-100 p-2 rounded-full'
                >
                    <FontAwesome name="close" size={20} color="#404CCF" />

                </TouchableOpacity>
            </View>

            <Text className='text-2xl font-bold text-primaryPurple text-center mt-2 mb-8'>
                Add a Common Place
            </Text>

            {/* form fields */}
            <View className='px-6 gap-6'>

                {/* location name input */}
                <View>
                    <Text className="text-primaryPurple font-bold text-base mb-2">Name</Text>
                    <View className='flex-row border items-center border-gray-300 bg-white rounded-lg px-3 py-3'>
                        <TextInput 
                            style={{ flex: 1, fontSize: 16, marginLeft: 10, color: 'black' }}
                            placeholder='Name this place (e.g. Office)'
                            value={name}
                            onChangeText={setName}
                        />
                    </View>
                </View>

                {/* address input */}
                <View>
                    <Text className="text-primaryPurple font-bold mb-2 text-base">Address</Text>
                    <AddressInput 
                        placeholder="Enter the address"
                        value={address}
                        onChangeText={setAddress}
                        onAddressSelect={handleAddressSelect}
                        mapboxAccessToken={MAPBOX_TOKEN || ''}
                        icon={<FontAwesome name="search" size={16} color="#6B7280" />}
                    />
                </View>
            </View>

            {/* map preview */}
            <View className='mt-6 w-full h-80 overflow-hidden'>
                <Mapbox.MapView
                    style={{ flex: 1 }}
                    styleURL={Mapbox.StyleURL.Street}
                    logoEnabled={false}
                    attributionEnabled={true}
                >

                    <Mapbox.Camera
                        zoomLevel={14}
                        centerCoordinate={coordinates || [0, 0]}
                        animationMode='flyTo'
                        animationDuration={1000}
                    />

                    {/* show a pin at the coordinates */}
                    {coordinates && (
                        <Mapbox.PointAnnotation
                            id="selectedLocation"
                            coordinate={coordinates}
                        >
                            <View className='bg-primaryPurple p-2 rounded-full border-2 border-white shadow-sm'>
                                <FontAwesome name="map-marker" size={20} color="white" />
                            </View>
                        </Mapbox.PointAnnotation>
                    )}
                </Mapbox.MapView>
            </View>
        </ScreenLayout>

    )
}

export default AddCommonPlaceScreen
