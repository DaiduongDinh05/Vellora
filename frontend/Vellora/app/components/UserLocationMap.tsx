import { StyleSheet, Text, View, ActivityIndicator } from 'react-native'
import React, { useState, useEffect } from 'react'
import Mapbox from '@rnmapbox/maps'
import * as Location from 'expo-location'

const MAPBOX_KEY = process.env.EXPO_PUBLIC_API_KEY_MAPBOX_PUBLIC_ACCESS_TOKEN;
Mapbox.setAccessToken(`${MAPBOX_KEY}`);

const UserLocationMap = () => {
    const [hasLocationPermission, setHasLocationPermission] = useState(false);
    const [initialCoordinate, setInitialCoordinate] = useState<[number, number] | null>(null);

    useEffect(() => {

        (async () => {
            let { status } = await Location.requestForegroundPermissionsAsync();
            if (status !== 'granted') {
                console.log('Permission to access location was denied');
                return;
            }
            setHasLocationPermission(true);

            let location = await Location.getCurrentPositionAsync({
                accuracy: Location.Accuracy.Highest,
            });
            setInitialCoordinate([location.coords.longitude, location.coords.latitude]);
        })();
    }, []);

    if (!initialCoordinate || !hasLocationPermission){
        return (
            <View style={styles.centerContainer}>
                <ActivityIndicator size="large" color="#4DBF69" />
                <Text style={{ marginTop: 10 }}>Finding your location...</Text>
            </View>
        );
    }

    return (
        <View style={styles.container}>
            <Mapbox.MapView 
                style={styles.map}
                // logoEnabled={false}
                attributionEnabled={false}
                styleURL={Mapbox.StyleURL.Street}
                rotateEnabled={false}
            >

                <Mapbox.Camera 
                    zoomLevel={16}
                    centerCoordinate={initialCoordinate}
                    animationMode={'none'}
                    // animationDuration={2000}
                    // followUserLocation={true}
                    // followUserMode={Mapbox.UserTrackingMode.Follow}
                
                />

                <Mapbox.UserLocation
                    visible={true}
                    animated={true}
                    showsUserHeadingIndicator={true}
                />
            </Mapbox.MapView>

        </View>
    );
};

const styles = StyleSheet.create({
    container:{
        flex: 1,
        overflow: 'hidden',
        borderRadius: 16,
    },
    map: {
        flex: 1,
    },
    centerContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#f5f5f5',
        borderRadius: 16,
    }


});
export default UserLocationMap
