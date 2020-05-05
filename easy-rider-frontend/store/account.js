export const state = () => ({
  pagingOptions: [5, 10, 15, 50],
  rowsPerPage: 5,
  locales: [{ value: 'en-US', text: 'English US (en-US)' }],
  locale: 'en-US',
  weekday: 1,
  weekdays: [
    { value: 0, text: 'Sunday' },
    { value: 1, text: 'Monday' },
    { value: 6, text: 'Saturday' }
  ],
  labels: {
    de: {
      labelPrevDecade: 'Vorheriges Jahrzehnt',
      labelPrevYear: 'Vorheriges Jahr',
      labelPrevMonth: 'Vorheriger Monat',
      labelCurrentMonth: 'Aktueller Monat',
      labelNextMonth: 'Nächster Monat',
      labelNextYear: 'Nächstes Jahr',
      labelNextDecade: 'Nächstes Jahrzehnt',
      labelToday: 'Heute',
      labelSelected: 'Ausgewähltes Datum',
      labelNoDateSelected: 'Kein Datum gewählt',
      labelCalendar: 'Kalender',
      labelNav: 'Kalendernavigation',
      labelHelp: 'Mit den Pfeiltasten durch den Kalender navigieren'
    },
    'ar-EG': {
      labelPrevDecade: 'العقد السابق',
      labelPrevYear: 'العام السابق',
      labelPrevMonth: 'الشهر السابق',
      labelCurrentMonth: 'الشهر الحالي',
      labelNextMonth: 'الشهر المقبل',
      labelNextYear: 'العام المقبل',
      labelNextDecade: 'العقد القادم',
      labelToday: 'اليوم',
      labelSelected: 'التاريخ المحدد',
      labelNoDateSelected: 'لم يتم اختيار تاريخ',
      labelCalendar: 'التقويم',
      labelNav: 'الملاحة التقويم',
      labelHelp: 'استخدم مفاتيح المؤشر للتنقل في التواريخ'
    },
    zh: {
      labelPrevDecade: '过去十年',
      labelPrevYear: '上一年',
      labelPrevMonth: '上个月',
      labelCurrentMonth: '当前月份',
      labelNextMonth: '下个月',
      labelNextYear: '明年',
      labelNextDecade: '下一个十年',
      labelToday: '今天',
      labelSelected: '选定日期',
      labelNoDateSelected: '未选择日期',
      labelCalendar: '日历',
      labelNav: '日历导航',
      labelHelp: '使用光标键浏览日期'
    }
  }
})

export const getters = {
  isPrivileged(state, getters, rootState) {
    if (!rootState.auth.loggedIn) {
      return false
    }

    const userRole = rootState.auth.user.role

    return userRole === 2 || userRole === 4
  },
  isAdmin(state, getters, rootState) {
    if (!rootState.auth.loggedIn) {
      return false
    }

    const userRole = rootState.auth.user.role

    return userRole === 4
  },
  availableRoleOptions(state, getters, rootState) {
    if (!rootState.auth.loggedIn) {
      return []
    }

    const userRole = rootState.auth.user.role

    if (userRole === 1) {
      return []
    } else if (userRole === 2) {
      return [
        { value: 1, text: 'USER' },
        { value: 2, text: 'MANAGER' }
      ]
    } else if (userRole === 4) {
      return [
        { value: 1, text: 'USER' },
        { value: 2, text: 'MANAGER' },
        { value: 4, text: 'ADMIN' }
      ]
    } else {
      return []
    }
  }
}

export const mutations = {
  setLocale(state, locale) {
    state.locale = locale
  },
  setStartWeekday(state, weekday) {
    state.weekday = weekday
  },
  setRowsPerPage(state, rowsPerPage) {
    state.rowsPerPage = rowsPerPage
  }
}
