# API Documentation: `/frontend_api/reservations`

## GET `/frontend_api/reservations`

List reservations with optional filters.

### Query Parameters

| Name                 | Type   | Description                                |
| -------------------- | ------ | ------------------------------------------ |
| `confirmationNumber` | string | Filter by confirmation number              |
| `lastName`           | string | Filter by guest’s last name (primary only) |
| `arrivalDate`        | string | Filter by arrival date (YYYY-MM-DD)        |
| `status`             | string | Filter by reservation status               |

### Response

```ts
type ReservationResponse = Array<{
  ReservationID: number;
  ConfirmationNumber: string;
  StatusCode: string;
  BookingChannelCode: string;
  PropertyID: number;
  profile?: {
    ProfileID: number;
    EmailAddress?: string;
    PhoneNumber?: string;
    nameInfo?: {
      FirstName: string;
      LastName: string;
      NamePrefix?: string;
    };
  };
  reservationStay?: {
    ArrivalDate: string;
    DepartureDate?: string;
    roomType?: {
      RoomTypeCode: string;
      Description: string;
    };
    room?: {
      RoomNumber: string;
    };
  };
}>;
```

---

## GET `/frontend_api/reservations/:id`

Get detailed reservation data.

### Response

```ts
type DetailedReservationResponse = {
  ReservationID: number;
  ConfirmationNumber: string;
  StatusCode: string;
  CancellationReason?: string;
  CancellationDate?: string;
  property: {
    PropertyName: string;
  };
  profile: {
    ProfileID: number;
    EmailAddress?: string;
    PhoneNumber?: string;
    nameInfos: Array<{
      FirstName: string;
      LastName: string;
      NamePrefix?: string;
    }>;
  };
  creator?: {
    FirstName: string;
    LastName: string;
  };
  reservationStays: Array<{
    ArrivalDate: string;
    DepartureDate: string;
    roomType: {
      RoomTypeCode: string;
      Description: string;
    };
    room: {
      RoomNumber: string;
    };
    guestNameInfos: Array<{
      nameInfo: {
        FirstName: string;
        LastName: string;
        NamePrefix?: string;
      };
    }>;
  }>;
};
```

---

## POST `/frontend_api/reservations`

Create a new reservation.

### Request

```ts
type CreateReservationRequest = {
  ConfirmationNumber: string;
  profile: {
    FirstName: string;
    LastName: string;
    EmailAddress?: string;
    PhoneNumber?: string;
  };
  reservationStays: Array<{
    ArrivalDate: string;
    DepartureDate: string;
    RoomTypeID: number;
    RoomID?: number;
  }>;
  BookingChannelCode: string;
  PropertyID: number;
};
```

### Response

```ts
type CreateReservationResponse = {
  ReservationID: number;
  confirmationNumber: string;
  guestName: string;
};
```

---

## PATCH `/frontend_api/reservations/:id`

Update reservation notes or stay details.

### Request

```ts
type PatchReservationRequest = {
  notes?: string;
  stays?: Array<{
    stayId: number;
    arrivalDate?: string;
    departureDate?: string;
    adultCount?: number;
    childCount?: number;
    roomTypeId?: number;
    rateAmount?: number;
  }>;
};
```

### Response

```ts
type UpdatedReservationResponse = DetailedReservationResponse;
```

---

## DELETE `/frontend_api/reservations/:id`

Cancel a reservation.

### Request

```ts
type CancelReservationRequest = {
  reason: string;
};
```

### Response

```ts
type CancelReservationResponse = {
  message: string;
};
```

---

## POST `/frontend_api/reservations/:id/check-in`

Check-in a guest.

### Request

```ts
type CheckInRequest = {
  roomId: number;
  guestDetails: {
    useReservedGuest: boolean;
    guests: Array<{
      firstName: string;
      lastName: string;
      idType?: string;
      idNumber?: string;
      isPrimary: boolean;
    }>;
  };
  paymentMethod: string;
  specialRequests?: string;
};
```

### Response

```ts
type CheckInResponse = {
  message: string;
  reservation: DetailedReservationResponse;
};
```

---

## POST `/frontend_api/reservations/:id/check-out`

Check-out a guest.

### Response

```ts
type CheckOutResponse = {
  message: string;
  reservation: DetailedReservationResponse;
};
```

---

## POST `/frontend_api/reservations/transform`

Remove redundant fields like `reservationStay` or `nameInfo`.

### Request

```ts
type TransformReservationsRequest = Array<any>; // full reservation list
```

### Response

Transformed version of reservations.

---

## POST `/frontend_api/reservations/optimize`

Same as `/transform`, optimized for storage/transmission.
