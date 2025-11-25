import { View, Text, StyleSheet } from "react-native";
import React from 'react';
import GeometryMap from "./GeometryMap";

// start address
// end address

// value - amount of miles

interface TripCardProps {
    geometry?: object | null;
    start_address: string;
    end_address: string;
    mileage_reimbursement_total: number;
    distance_meters: number;
}

const TripCard: React.FC<TripCardProps> = ({ geometry, start_address, end_address, mileage_reimbursement_total, distance_meters }) => {

    return (
        <View style={styles.cardContainer}>
            <View style={styles.mapContainer}>
                <GeometryMap geometry={geometry}/>
            </View>
            <View style={styles.textContainer}>
                <View style={styles.addressTextContainer}> 
                    <Text style={{flexWrap: 'wrap', flex: 1, fontSize: 12}}>{'\u2022'} {start_address}</Text>
                    <Text style={{flexWrap: 'wrap', flex: 1, fontSize: 12}}>{'\u2022'} {end_address}</Text>
                </View>
                <View style={{marginBottom: 40, marginLeft: 40}}>
                    <Text style={{color: '#4DBF69'}}>${mileage_reimbursement_total} - {distance_meters} mi</Text>
                </View>
            </View>
        </View>
    )
}

const styles = StyleSheet.create({
    cardContainer: {
        justifyContent: 'flex-start',
        alignItems: 'center',
        alignContent: 'center',
        width: '100%',
        height: '10%',
        flexDirection: 'row',
        borderTopWidth: 1.5,
        borderColor: '#b5b5b5',
        padding: 40,
        backgroundColor: 'white'
    },
    mapContainer: {
        height: 115, 
        width: 115, 
        overflow: 'hidden', 
        borderRadius: 10, 
        flexShrink: 0 
    },
    textContainer: {
        flex: 1, 
        marginLeft: 10,
        marginTop: 10
    },
    addressTextContainer: {
        marginBottom: 30, 
        marginTop: 20
    },

});


export default TripCard