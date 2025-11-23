import { View, Text, Pressable } from "react-native";
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
        <View style={{justifyContent: 'flex-start', alignItems: 'center', width: '100%', height: '20%', flexDirection:'row', borderTopWidth: 2, borderBottomWidth: 2, borderColor: 'gray'}}>
            <View style={{ height: 125, width: 125, overflow: 'hidden', borderRadius: 10, marginLeft: 30 }}>
                <GeometryMap geometry={geometry}/>
            </View>
            <View>
                <View style={{marginBottom: 40, marginLeft: 10, marginTop: 20}}> 
                    <Text>{'\u2022'} {start_address}</Text>
                    <Text>{'\u2022'} {end_address}</Text>
                </View>
                <View style={{marginBottom: 40, marginLeft: 50}}>
                    <Text style={{color: '#4DBF69'}}>${mileage_reimbursement_total} - {distance_meters} mi</Text>
                </View>
            </View>
        </View>
    )
}


export default TripCard