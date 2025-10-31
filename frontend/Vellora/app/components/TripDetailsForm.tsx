import { View } from 'react-native'
import React from 'react'
import { FontAwesome } from '@expo/vector-icons'
import NoteInput from './NoteInput'
import Dropdown from './Dropdown'
import CurrencyInput from './CurrencyInput'
import FilledAddressBox from './FilledAddressBox'


type TripDtailsFormProps = {
    notes: string,
    setNotes: (value: string) => void;

    vehicle: string | null;
    setVehicle: (value: string | null) => void;

    type: string | null;
    setType: (value: string | null) => void;

    rate: string | null;
    setRate: (value: string | null) => void;

    parking: string;
    setParking: (value: string) => void;

    gas: string;
    setGas: (value: string) => void;

    startAddress?: string;
    setStartAddress?: (value: string) => void;

    endAddress?: string;
    setEndAddress?: (value: string) => void;

    tolls?: string;
    setTolls?: (value: string) => void;

    vehicleItems: any[];
    typeItems: any[];
    rateItems: any[];

    
};

const TripDetailsForm: React.FC<TripDtailsFormProps> = (props) => {

    const iconProps = { size: 18 };

    return (
        <View style={{ padding: 25, gap: 16 }}>
            {props.startAddress !== undefined && props.setStartAddress && (
                <FilledAddressBox 
                    value={props.startAddress}
                    onChangeText={props.setStartAddress}
                />
            )}
            {props.endAddress !== undefined && props.setEndAddress && (
                <FilledAddressBox 
                    value={props.endAddress}
                    onChangeText={props.setEndAddress}
                />
            )}


            {/* render notes input */}
            <NoteInput 
                placeholder="Add your crazy notes"
                value={props.notes}
                onChangeText={props.setNotes}
                className=''
            />

            <View className='flex-row gap-4'>
                <CurrencyInput 
                    label='Parking'
                    value={props.parking}
                    onChangeText={props.setParking}
                    className="flex-1"
                />
                
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
