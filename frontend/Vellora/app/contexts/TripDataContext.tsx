import React, { createContext, useContext, useState, ReactNode } from 'react';

export interface TripData {
    notes: string;
    vehicle: string | null;
    type: string | null;
    rate: string | null;
    parking: string;
    gas: string;
    tolls?: string;
    startAddress?: string;
    endAddress?: string;
    distance?: string;
    value?: string;
}

interface TripDataContextType {
    tripData: TripData;
    updateTripData: (updates: Partial<TripData>) => void;
    resetTripData: () => void;
}

const defaultTripData: TripData = {
    notes: '',
    vehicle: null,
    type: null,
    rate: null,
    parking: '',
    gas: '',
    tolls: '',
    startAddress: '',
    endAddress: '',
    distance: '0',
    value: '0.00'
};

const TripDataContext = createContext<TripDataContextType | undefined>(undefined);

export const TripDataProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [tripData, setTripData] = useState<TripData>(defaultTripData);

    const updateTripData = (updates: Partial<TripData>) => {
        setTripData(prev => ({ ...prev, ...updates }));
    };

    const resetTripData = () => {
        setTripData(defaultTripData);
    };

    return (
        <TripDataContext.Provider value={{ tripData, updateTripData, resetTripData }}>
            {children}
        </TripDataContext.Provider>
    );
};

export const useTripData = () => {
    const context = useContext(TripDataContext);
    if (context === undefined) {
        throw new Error('useTripData must be used within a TripDataProvider');
    }
    return context;
};