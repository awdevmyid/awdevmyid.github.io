function keepAlive() {
    // Send "keep alive" signal to server
    fetch("/keep-alive");

    // Set timeout to send signal again after 60 seconds
    setTimeout(keepAlive, 60000);
  }

  // Start sending "keep alive" signals
  keepAlive();
