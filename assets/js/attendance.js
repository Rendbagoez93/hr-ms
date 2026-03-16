document.addEventListener("DOMContentLoaded", () => {
  const timeEl = document.getElementById("attendance-live-time");
  const dateEl = document.getElementById("attendance-live-date");
  const statusFilter = document.getElementById("status-filter");
  const table = document.getElementById("attendance-table");

  const refreshClock = () => {
    if (!timeEl || !dateEl) {
      return;
    }

    const now = new Date();
    timeEl.textContent = now.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
    dateEl.textContent = now.toLocaleDateString([], {
      weekday: "short",
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  };

  const applyLocalStatusFilter = () => {
    if (!statusFilter || !table) {
      return;
    }

    const selectedStatus = statusFilter.value;
    const rows = table.querySelectorAll("tbody tr[data-status]");

    rows.forEach((row) => {
      const rowStatus = row.getAttribute("data-status") || "";
      const shouldShow = !selectedStatus || rowStatus === selectedStatus;
      row.hidden = !shouldShow;
    });
  };

  refreshClock();
  window.setInterval(refreshClock, 1000);

  if (statusFilter) {
    statusFilter.addEventListener("change", applyLocalStatusFilter);
  }
});
