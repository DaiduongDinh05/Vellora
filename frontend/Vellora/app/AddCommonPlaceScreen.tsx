import { Text, View } from 'react-native'
import React from 'react'
import Mapbox from '@rnmapbox/maps';
import { useRouter } from 'expo-router';

const MAPBOX_TOKEN = process.env.EXPO_PUBLIC_API_KEY_MAPBOX_PUBLIC_ACCESS_TOKEN;
Mapbox.setAccessToken(`${MAPBOX_TOKEN}`);

const AddCommonPlaceScreen = () => {
    const router = useRouter();
    
    return (
        <View>
            <Text>AddCommonPlaceScreen</Text>
        </View>
    )
}

export default AddCommonPlaceScreen
