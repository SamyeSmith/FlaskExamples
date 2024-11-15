document.addEventListener('DOMContentLoaded', () => {
                            const form = document.querySelector('form');
                            const passwordInput = form.querySelector('input[name="password"]');
                            const errorMessage = document.createElement('p');
                          
                            errorMessage.style.color = 'red';
                            errorMessage.style.fontSize = '14px';
                            errorMessage.style.display = 'none';
                            form.insertBefore(errorMessage, form.querySelector('.login-btn'));
                          
                            form.addEventListener('submit', (event) => {
                              if (passwordInput.value.length < 8) {
                                event.preventDefault(); // Prevent form submission
                                errorMessage.textContent = 'Password must be at least 8 characters long.';
                                errorMessage.style.display = 'block';
                              } else {
                                errorMessage.style.display = 'none';
                              }
                            });
                          });
                          