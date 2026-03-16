(() => {
  const CLOCK_KEY = "__attendanceClockIntervalId";

  const stopPreviousClock = () => {
    const previousId = window[CLOCK_KEY];
    if (previousId) {
      window.clearInterval(previousId);
      window[CLOCK_KEY] = null;
    }
  };

  const initClock = () => {
    const timeEl = document.getElementById("attendance-live-time");
    const dateEl = document.getElementById("attendance-live-date");

    stopPreviousClock();

    if (!timeEl || !dateEl) {
      return;
    }

    const refreshClock = () => {
      const now = new Date();
      timeEl.textContent = now.toLocaleTimeString(undefined, {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
      });
      dateEl.textContent = now.toLocaleDateString(undefined, {
        weekday: "short",
        year: "numeric",
        month: "short",
        day: "numeric",
      });
    };

    refreshClock();
    window[CLOCK_KEY] = window.setInterval(refreshClock, 1000);
  };

  document.addEventListener("DOMContentLoaded", initClock);
  document.addEventListener("htmx:afterSwap", initClock);
})();
