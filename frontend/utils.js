import moment from "moment";

moment.locale(navigator.language);
export function calendarDate(date) {
    return moment.parseZone(date).calendar(null, {
        lastDay: '[Yesterday at] HH:mm',
        sameDay: '[Today at] HH:mm',
        nextDay: '[Tomorrow at] HH:mm',
        lastWeek: '[Last] dddd [at] HH:mm',
        nextWeek: 'dddd [at] HH:mm',
        sameElse: 'L [at] HH:mm'
    });
}

export function isLocalStorageAvailable() {
    // https://stackoverflow.com/questions/16427636/check-if-localstorage-is-available
    if (typeof localStorage !== 'undefined') {
        try {
            localStorage.setItem('feature_test', 'yes');
            if (localStorage.getItem('feature_test') === 'yes') {
                localStorage.removeItem('feature_test');
                return true
            } else {
                return false
            }
        } catch (e) {
            return false
        }
    }

    return false
}

export const hasLocalStorage = isLocalStorageAvailable()
