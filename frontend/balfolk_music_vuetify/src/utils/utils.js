import axios from 'axios';

export const get_upcoming_events = (objects) => {
    let now = new Date().getTime();
    function is_upcoming(event) {
        return new Date(event.ending_datetime).getTime() >= now;
    }
    return objects.filter(is_upcoming);
}

export const get_past_events = (objects) => {
    let now = new Date().getTime();
    function is_past(event) {
        return new Date(event.ending_datetime).getTime() < now;
    }
    return objects.filter(is_past).reverse();
}

export const getWeekdayStart = (obj) => {
    let date = new Date(obj.starting_datetime);
    return date.toLocaleDateString('en-US', { weekday: 'short' });
}

export const getDayOfMonthStart = (obj) => {
    let date = new Date(obj.starting_datetime);
    return date.getDate();
}

export const getMonthStart = (obj) => {
    let date = new Date(obj.starting_datetime);
    return date.toLocaleDateString('en-US', { month: 'short' }).toUpperCase();
}

export async function fetchEventData(event_type, objects, loading) {
    loading.value = true;
    var response = await axios.get("/events/?event_type=" + event_type);
    objects.value = response.data;
    loading.value = false;
}
