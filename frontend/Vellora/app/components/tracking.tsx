import React from 'react'
import {  View, Text, Button  } from "react-native";
import { useState, useEffect } from "react";
import * as Location from 'expo-location';
import * as TaskManager from 'expo-task-manager';

const LOCATION_TASK_NAME = 'background_location_tracking';
let coordinates = '';                                       // initalize the empty string
const PROFILE = 'mapbox/driving';                           // profile for mapbox api

TaskManager.defineTask(LOCATION_TASK_NAME, async ({ data, error }) => {
        if (error) {
            console.log('Background Location tasks Error: ', error.message)
            return;
        }

        try {
              const { locations } = data as { locations: Location.LocationObject[] }; 
              console.log(locations);

            

              let lat = locations[0].coords.latitude.toString();
              let long = locations[0].coords.longitude.toString();

              if (coordinates.length > 500) { // API Limitation
                // API Limitation Logic here
              }
              else {
                coordinates += lat + ',' + long + ';'; // Making the semi colon separated list for the API Call
              }
              
              console.log('Coordinate String: ', coordinates);

              
        } catch (err) {
            console.error('Error with location update:', err);
        }
                
            });

function LocationTracker()  { 
    const [errorMessage, setErrorMessage] = useState<string | null>(null);
    const [isTracking, setIsTracking] = useState(false);

    async function getPermissions() {
        try {
                const { status: foregroundPermissions } = await Location.requestForegroundPermissionsAsync(); // have to request Foreground before BG
                        if (!foregroundPermissions) { // Check if Granted
                                setErrorMessage('Permission to access location was denied. Please enable location.');
                                return false;
                        }

                        let { status: backgroundPermssions } = await Location.requestBackgroundPermissionsAsync(); // Request Background Location for Tracking
                        if (backgroundPermssions !== "granted" ) {
                                setErrorMessage('Permission to access background location was denied, Please enable background location for best performance.')
                                return false;
                        }
        return true;

        } catch (error) {
                console.error('Error getting permissions: ', error)
                return false;
        }
    }

    async function startTracking() {
        try {
            // Get Perms for Location Tracking
            const hasPermissions = await getPermissions();
            if (!hasPermissions) return;

            await Location.startLocationUpdatesAsync(LOCATION_TASK_NAME, {
                accuracy: Location.Accuracy.BestForNavigation,
                timeInterval: 10,
                distanceInterval: 200, // was: 1610 ~1 mile TODO: MODIFY THIS VALUE TO MAKE ACCURATE LOCATION UPDATES
                // For android to allow background location services
                foregroundService: {
                    notificationTitle: 'Location Tracking is Active',
                    notificationBody: 'Your Location is being tracked in the background.',
                },
            });

            setIsTracking(true);

            
        } catch (error) {
            console.error('Error to start tracking: ', error);
            setIsTracking(false);
            return;
        }
    };

    async function stopTracking() {
        try {
            if (isTracking) {
                const isStopped = await Location.stopLocationUpdatesAsync(LOCATION_TASK_NAME);
                console.log("Tracking stopped.");
                setIsTracking(false);
            }
        } catch (error) {
            console.error('Error to stop tracking: ', error);
            setIsTracking(false);
            return;
        }
    };




    useEffect(() => {
       startTracking(); 

       return () => { // useEffect Cleanup Function to stop tracking location when Component dismounts
            if (isTracking) {
                stopTracking();
                return;
            }
       };
    }, []);



    return (
        <View>
            <Button title="Start Tracking" onPress={startTracking} />
            <Button title="Stop Tracking" onPress={stopTracking} />
            {isTracking ? (
                <Text>Tracking is active</Text>
            ) : (
                <Text>Tracking is inactive</Text>
            )}
        </View>
      
    )
}



export default LocationTracker;