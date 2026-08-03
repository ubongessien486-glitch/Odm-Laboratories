const WEB3FORM_RECIPIENTS = [
  { label: 'ubongessien486@gmail.com', accessKey: '6ca01595-fa75-4d60-a4b5-2f8a9aee2c3d' },
  { label: 'rmetim@icloud.com', accessKey: '65a653a7-6d77-4943-b442-2f260216a7b8' }
];

const wait = (delay) => new Promise((resolve) => {
  window.setTimeout(resolve, delay);
});

async function submitToWeb3Forms(recipient, fields) {
  const formData = new FormData();
  formData.append('access_key', recipient.accessKey);

  Object.entries(fields).forEach(([key, value]) => {
    formData.append(key, value ?? '');
  });

  const response = await fetch('https://api.web3forms.com/submit', {
    method: 'POST',
    body: formData
  });

  if (!response.ok) {
    throw new Error(`Web3Forms returned ${response.status}`);
  }

  const result = await response.json().catch(() => ({}));
  if (result.success === false) {
    throw new Error(result.message || 'Web3Forms rejected the submission.');
  }

  return result;
}

export async function sendWeb3FormsNotification(fields) {
  const results = [];
  const failures = [];

  for (const recipient of WEB3FORM_RECIPIENTS) {
    let delivered = false;
    let lastError = null;

    for (let attempt = 1; attempt <= 2; attempt += 1) {
      try {
        const result = await submitToWeb3Forms(recipient, fields);
        results.push({ recipient: recipient.label, result });
        delivered = true;
        break;
      } catch (error) {
        lastError = error;
        if (attempt < 2) {
          await wait(1200);
        }
      }
    }

    if (!delivered) {
      failures.push(`${recipient.label}: ${lastError?.message || 'unknown error'}`);
    }

    await wait(500);
  }

  if (failures.length) {
    throw new Error(`Web3Forms failed for ${failures.join('; ')}`);
  }

  return {
    successful: results.length,
    failed: failures.length,
    results
  };
}
