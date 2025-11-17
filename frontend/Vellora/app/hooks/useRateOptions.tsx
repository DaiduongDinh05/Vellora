import { useState, useEffect } from 'react';
import { getRateCustomizations, RateCustomization } from '../services/rateCustomizations';

export const useRates = () => {
    const [rates, setRates] = useState<RateCustomization[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchRates = async () => {
        try {
            setLoading(true);
            setError(null);
            const userRates = await getRateCustomizations();
            setRates(userRates);

        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to fetch rates');
            console.error('Error fetching rates:', err);

        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchRates();
    }, []);

    // transform rates for dropdown format
    const rateItems = rates.map(rate => ({
        label: `${rate.name} (${rate.year})`,
        value: rate.id,                         // Using the UUID as value
        originalRate: rate,
    }));

    return {
        rates,
        rateItems,
        loading,
        error,
        refreshRates: fetchRates,
    };
};