import { View } from 'react-native';
import React from 'react';
import { FontAwesome } from '@expo/vector-icons';

// import custom components
import NoteInput from './NoteInput';
import Dropdown from './Dropdown';
import CurrencyInput from './CurrencyInput';

// typescript type for expected props
type TripDtailsFormProps = {

    // notes text input
    notes: string,
    setNotes: (value: string) => void;

    // vehicle choice
    vehicle: string | null;
    setVehicle: (value: string | null) => void;

    // type/category choice
    type: string | null;
    setType: (value: string | null) => void;

    // reimbursement rate choice
    rate: string | null;
    setRate: (value: string | null) => void;

    // parking cost input
    parking: string;
    setParking: (value: string) => void;

    // gas cost input
    gas: string;
    setGas: (value: string) => void;

    // optional start address
    startAddress?: string;
    setStartAddress?: (value: string) => void;

    // optional end address
    endAddress?: string;
    setEndAddress?: (value: string) => void;

    // optional tolls
    tolls?: string;
    setTolls?: (value: string) => void;

    // test arrays for dropdown data
    vehicleItems: any[];
    typeItems: any[];
    rateItems: any[];

    
};

// this is a reusable controlled component that does not manage its own data (but receives it in props)
// is used to create forms when starting, updating, or ending trip details
const TripDetailsForm: React.FC<TripDtailsFormProps> = (props) => {

    // common icon properties
    const iconProps = { size: 18 };

    return (
        <View style={{ padding: 25, gap: 16 }}>

            {/* Conditionally render start and end addresses (only if those props are provided) */}
            {props.startAddress !== undefined && props.setStartAddress && (
                <NoteInput 
                    value={props.startAddress}
                    onChangeText={props.setStartAddress}
                    placeholder='Select Start Location...'
                />
            )}
            {props.endAddress !== undefined && props.setEndAddress && (
                <NoteInput 
                    value={props.endAddress}
                    onChangeText={props.setEndAddress}
                    placeholder='Select End Location...'

                />
            )}


            {/* render multiline notes input */}
            <NoteInput 
                multiline
                placeholder="Add your crazy notes"
                value={props.notes}
                onChangeText={props.setNotes}
                className=''
            />

            {/* render currency type inputs */}
            <View className='flex-row gap-4'>
                <CurrencyInput 
                    label='Parking'
                    value={props.parking}
                    onChangeText={props.setParking}
                    className="flex-1"
                />
                
                {/* conditionally render tolls if the tolls prop is provided. If not, render gas instead     */}
                {props.tolls !== undefined && props.setTolls ? (
                    <CurrencyInput 
                        label='Tolls'
                        value={props.tolls}
                        onChangeText={props.setTolls}
                        className="flex-1"
                    />
                ) : (
                    <CurrencyInput 
                        label='Gas'
                        value={props.gas}
                        onChangeText={props.setGas}
                        className="flex-1"
                    />
                )}
            </View>

            {/* if tolls were rendered earlier, also render gas */}
            {props.tolls !== undefined && (
                <CurrencyInput 
                    label='Gas'
                    value={props.gas}
                    onChangeText={props.setGas}
                    className="flex-1"
                />
            )}

            {/* render vehicle dropdown */}
            <Dropdown 
                placeholder="Select vehicle"
                items={props.vehicleItems}
                onValueChange={props.setVehicle}
                value={props.vehicle}
                icon={<FontAwesome name="car" {...iconProps} />}
            />

            {/* render type dropdown */}
            <Dropdown 
                placeholder="Select type"
                items={props.typeItems}
                onValueChange={props.setType}
                value={props.type}
                icon={<FontAwesome name="list-ul" {...iconProps} />}
            />

            {/* render rate dropdown */}
            <Dropdown 
                placeholder="Select reimbursement rate"
                items={props.rateItems}
                onValueChange={props.setRate}
                value={props.rate}
                icon={<FontAwesome name="dollar" {...iconProps} />}
            />
        
        </View>
    )
}

export default TripDetailsForm
