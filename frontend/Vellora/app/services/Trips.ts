import { API_BASE_URL } from "../constants/api";
import { tokenStorage } from "./tokenStorage";

export type Expense = {
    id: string;
    type: string;
    amount: number;
    createdAt: Date;
}

export enum TripStatus {
    Active,
    Completed,
    Cancelled
}

export type Trip = {
    id: string;
    userId: string;
    status: TripStatus;
    startAddress: string;
    endAddress: string;
    purpose?: string;
    reimbursementRate: number;
    miles: number;
    geometry?: object | null;
    mileageReimbursementTotal: number;
    expenseReimbursementTotal: number;
    startAt: Date;
    endAt?: Date | undefined;
    updatedAt: Date;
    rateCustomizationId: string;
    rateCategoryId: string;
    expenses?: Expense[] | null;
}

 // Types for payloads for Backend API calls
export type createTripPayload = {
    startAddress: string;
    purpose?: string | null;
    vechicle?: string | null;
    rateCustomizationId: string;
    rateCategoryId: string;
}


export type createManualTripPayload = {
    startAddress: string;
    endAddress: string;
    startedAt: Date;
    endedAt: Date;
    miles: number;
    geometry: object | null;
    rateCustomizationId: string;
    rateCategoryId: string;
    expenses: Expense[];
}