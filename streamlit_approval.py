# import streamlit as st
# import requests
# import jwt
# from datetime import datetime
# import os
# from urllib.parse import urlparse

# # Page config
# st.set_page_config(
#     page_title="Podcast Approval System",
#     page_icon="🎙️",
#     layout="centered",
#     initial_sidebar_state="collapsed"
# )

# # Custom CSS
# st.markdown("""
# <style>
#     .stApp {
#         background-color: #f8f9fa;
#     }
#     .success-container {
#         background-color: #d4edda;
#         border: 1px solid #c3e6cb;
#         border-radius: 10px;
#         padding: 30px;
#         text-align: center;
#         margin: 20px 0;
#     }
#     .error-container {
#         background-color: #f8d7da;
#         border: 1px solid #f5c6cb;
#         border-radius: 10px;
#         padding: 30px;
#         text-align: center;
#         margin: 20px 0;
#     }
#     .info-container {
#         background-color: #d1ecf1;
#         border: 1px solid #bee5eb;
#         border-radius: 10px;
#         padding: 30px;
#         margin: 20px 0;
#     }
#     .big-emoji {
#         font-size: 72px;
#         margin-bottom: 20px;
#     }
#     .status-text {
#         font-size: 24px;
#         font-weight: bold;
#         margin-bottom: 10px;
#     }
#     .details-text {
#         font-size: 16px;
#         color: #666;
#     }
# </style>
# """, unsafe_allow_html=True)

# def decode_token(token):
#     """Decode JWT token without verification (for display purposes)"""
#     try:
#         # Decode without verification to extract payload
#         decoded = jwt.decode(token, options={"verify_signature": False})
#         return decoded
#     except Exception as e:
#         st.error(f"Failed to decode token: {str(e)}")
#         return None

# def process_approval(token):
#     """Process the approval by calling the backend API"""
#     try:
#         # Decode token to get backend URL
#         token_data = decode_token(token)
#         if not token_data:
#             return False, "Invalid token format"
        
#         # Get backend URL from token or use environment variable
#         backend_url = "https://c15ccbaa9f46.ngrok-free.app"
        
#         # Remove any trailing slashes
#         backend_url = backend_url.rstrip('/')
        
#         # Construct the approval endpoint
#         approval_endpoint = f"{backend_url}/api/v1/approval/action"
        
#         # Make the API call
#         response = requests.get(
#             approval_endpoint,
#             params={'token': token},
#             timeout=30
#         )
        
#         if response.status_code == 200:
#             return True, "Approval processed successfully"
#         else:
#             error_msg = "Failed to process approval"
#             try:
#                 error_data = response.json()
#                 if 'error' in error_data:
#                     error_msg = error_data['error']
#             except:
#                 error_msg = f"Server error: {response.status_code}"
#             return False, error_msg
            
#     except requests.exceptions.ConnectionError:
#         return False, "Cannot connect to the backend server. Please try again later."
#     except requests.exceptions.Timeout:
#         return False, "Request timed out. Please try again."
#     except Exception as e:
#         return False, f"An error occurred: {str(e)}"

# def main():
#     # Get token from URL parameters
#     query_params = st.experimental_get_query_params()
#     token = query_params.get('token', [None])[0]
    
#     # Header
#     st.markdown("<h1 style='text-align: center; color: #007bff;'>🎙️ Podcast Approval System</h1>", unsafe_allow_html=True)
    
#     if not token:
#         # No token provided
#         st.markdown("""
#         <div class="error-container">
#             <div class="big-emoji">❌</div>
#             <div class="status-text">Invalid Approval Link</div>
#             <div class="details-text">
#                 No approval token was provided. Please use the link from your approval email.
#             </div>
#         </div>
#         """, unsafe_allow_html=True)
#         return
    
#     # Decode token to show details
#     token_data = decode_token(token)
    
#     if token_data:
#         # Check if token is expired
#         exp_timestamp = token_data.get('exp', 0)
#         if exp_timestamp and datetime.utcnow().timestamp() > exp_timestamp:
#             st.markdown("""
#             <div class="error-container">
#                 <div class="big-emoji">⏰</div>
#                 <div class="status-text">Approval Link Expired</div>
#                 <div class="details-text">
#                     This approval link has expired. Please request a new approval email.
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)
#             return
        
#         # Show approval details
#         job_id = token_data.get('job_id', 'Unknown')
#         stage = token_data.get('stage', 'Unknown').title()
#         action = token_data.get('action', 'Unknown').title()
        
#         # Display approval information
#         st.markdown(f"""
#         <div class="info-container">
#             <h3>Approval Details</h3>
#             <p><strong>Job ID:</strong> {job_id}</p>
#             <p><strong>Stage:</strong> {stage}</p>
#             <p><strong>Action:</strong> {action}</p>
#         </div>
#         """, unsafe_allow_html=True)
        
#         # Process button
#         col1, col2, col3 = st.columns([1, 2, 1])
#         with col2:
#             if st.button(f"Confirm {action}", type="primary", use_container_width=True):
#                 # Process the approval
#                 with st.spinner('Processing your approval...'):
#                     success, message = process_approval(token)
                
#                 if success:
#                     st.balloons()
#                     st.markdown(f"""
#                     <div class="success-container">
#                         <div class="big-emoji">✅</div>
#                         <div class="status-text">{action}d Successfully!</div>
#                         <div class="details-text">
#                             The {stage.lower()} has been {action.lower()}d for job {job_id}.
#                             <br><br>
#                             You can now close this window. The podcast pipeline will continue automatically.
#                         </div>
#                     </div>
#                     """, unsafe_allow_html=True)
#                 else:
#                     st.markdown(f"""
#                     <div class="error-container">
#                         <div class="big-emoji">❌</div>
#                         <div class="status-text">Error Processing Approval</div>
#                         <div class="details-text">
#                             {message}
#                             <br><br>
#                             Please contact support if you continue to experience issues.
#                         </div>
#                     </div>
#                     """, unsafe_allow_html=True)
#     else:
#         # Invalid token
#         st.markdown("""
#         <div class="error-container">
#             <div class="big-emoji">🔒</div>
#             <div class="status-text">Invalid Token</div>
#             <div class="details-text">
#                 The approval token is invalid or corrupted. Please use the link from your approval email.
#             </div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     # Footer
#     st.markdown("---")
#     st.markdown("<p style='text-align: center; color: #666;'>Podcast Generation System © 2024</p>", unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()
import streamlit as st
import requests
import jwt
from datetime import datetime
import os
from urllib.parse import urlparse
import json

# Page config
st.set_page_config(
    page_title="Podcast Approval System",
    page_icon="🎙️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #f8f9fa;
    }
    .success-container {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 10px;
        padding: 30px;
        text-align: center;
        margin: 20px 0;
    }
    .error-container {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 10px;
        padding: 30px;
        text-align: center;
        margin: 20px 0;
    }
    .info-container {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 10px;
        padding: 30px;
        margin: 20px 0;
    }
    .big-emoji {
        font-size: 72px;
        margin-bottom: 20px;
    }
    .status-text {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .details-text {
        font-size: 16px;
        color: #666;
    }
    .debug-info {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
        font-family: monospace;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

def decode_token(token):
    """Decode JWT token without verification (for display purposes)"""
    try:
        # Decode without verification to extract payload
        decoded = jwt.decode(token, options={"verify_signature": False})
        return decoded
    except Exception as e:
        st.error(f"Failed to decode token: {str(e)}")
        return None

def test_backend_connection():
    """Test if backend is reachable"""
    try:
        backend_url = "https://c15ccbaa9f46.ngrok-free.app"
        test_url = f"{backend_url}/api/v1/approval/test"
        
        response = requests.get(
            test_url,
            headers={
                'ngrok-skip-browser-warning': 'true',
                'User-Agent': 'StreamlitApp/1.0'
            },
            timeout=10
        )
        
        if response.status_code == 200:
            return True, "Backend is reachable"
        else:
            return False, f"Backend returned status {response.status_code}: {response.text}"
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to backend - connection refused"
    except requests.exceptions.Timeout:
        return False, "Backend connection timeout"
    except Exception as e:
        return False, f"Backend test failed: {str(e)}"

def process_approval(token):
    """Process the approval by calling the backend API"""
    try:
        # Decode token to get backend URL
        token_data = decode_token(token)
        if not token_data:
            return False, "Invalid token format"
        
        # Get backend URL from token or use environment variable
        backend_url = "https://c15ccbaa9f46.ngrok-free.app"
        
        # Remove any trailing slashes
        backend_url = backend_url.rstrip('/')
        
        # Construct the approval endpoint
        approval_endpoint = f"{backend_url}/api/v1/approval/action"
        
        # Prepare headers for ngrok
        headers = {
            'Content-Type': 'application/json',
            'ngrok-skip-browser-warning': 'true',
            'User-Agent': 'StreamlitApp/1.0'
        }
        
        st.write(f"🔄 Sending request to: {approval_endpoint}")
        st.write(f"🔧 Headers: {headers}")
        
        # Make the API call
        response = requests.get(
            approval_endpoint,
            params={'token': token},
            headers=headers,
            timeout=30
        )
        
        st.write(f"📡 Response status: {response.status_code}")
        st.write(f"📝 Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                response_data = response.json()
                st.write(f"✅ Response data: {response_data}")
                return True, response_data.get('message', 'Approval processed successfully')
            except json.JSONDecodeError:
                st.write(f"⚠️ Response text: {response.text}")
                return True, "Approval processed successfully"
        else:
            error_msg = "Failed to process approval"
            try:
                error_data = response.json()
                if 'error' in error_data:
                    error_msg = error_data['error']
                st.write(f"❌ Error response: {error_data}")
            except:
                error_msg = f"Server error: {response.status_code} - {response.text}"
                st.write(f"❌ Raw error response: {response.text}")
            return False, error_msg
            
    except requests.exceptions.ConnectionError as e:
        error_msg = f"Cannot connect to the backend server: {str(e)}"
        st.write(f"🔌 Connection error: {error_msg}")
        return False, error_msg
    except requests.exceptions.Timeout:
        error_msg = "Request timed out. Please try again."
        st.write(f"⏰ Timeout error: {error_msg}")
        return False, error_msg
    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        st.write(f"💥 Unexpected error: {error_msg}")
        return False, error_msg

def main():
    # Get token from URL parameters
    query_params = st.experimental_get_query_params()
    token = query_params.get('token', [None])[0]
    
    # Header
    st.markdown("<h1 style='text-align: center; color: #007bff;'>🎙️ Podcast Approval System</h1>", unsafe_allow_html=True)
    
    # Debug section (collapsible)
    with st.expander("🔍 Debug Information", expanded=False):
        st.write("**Query Parameters:**", query_params)
        st.write("**Token (first 50 chars):**", token[:50] if token else "None")
        
        # Test backend connection
        st.write("**Backend Connection Test:**")
        backend_ok, backend_msg = test_backend_connection()
        if backend_ok:
            st.success(f"✅ {backend_msg}")
        else:
            st.error(f"❌ {backend_msg}")
    
    if not token:
        # No token provided
        st.markdown("""
        <div class="error-container">
            <div class="big-emoji">❌</div>
            <div class="status-text">Invalid Approval Link</div>
            <div class="details-text">
                No approval token was provided. Please use the link from your approval email.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Decode token to show details
    token_data = decode_token(token)
    
    if token_data:
        # Check if token is expired
        exp_timestamp = token_data.get('exp', 0)
        if exp_timestamp and datetime.utcnow().timestamp() > exp_timestamp:
            st.markdown("""
            <div class="error-container">
                <div class="big-emoji">⏰</div>
                <div class="status-text">Approval Link Expired</div>
                <div class="details-text">
                    This approval link has expired. Please request a new approval email.
                </div>
            </div>
            """, unsafe_allow_html=True)
            return
        
        # Show approval details
        job_id = token_data.get('job_id', 'Unknown')
        stage = token_data.get('stage', 'Unknown').title()
        action = token_data.get('action', 'Unknown').title()
        
        # Display approval information
        st.markdown(f"""
        <div class="info-container">
            <h3>Approval Details</h3>
            <p><strong>Job ID:</strong> {job_id}</p>
            <p><strong>Stage:</strong> {stage}</p>
            <p><strong>Action:</strong> {action}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show backend status
        backend_ok, backend_msg = test_backend_connection()
        if not backend_ok:
            st.error(f"⚠️ Backend Issue: {backend_msg}")
        
        # Process button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(f"Confirm {action}", type="primary", use_container_width=True):
                # Process the approval
                with st.spinner('Processing your approval...'):
                    # Show debug information during processing
                    with st.expander("🔧 Processing Details", expanded=True):
                        success, message = process_approval(token)
                
                if success:
                    st.balloons()
                    st.markdown(f"""
                    <div class="success-container">
                        <div class="big-emoji">✅</div>
                        <div class="status-text">{action}d Successfully!</div>
                        <div class="details-text">
                            The {stage.lower()} has been {action.lower()}d for job {job_id}.
                            <br><br>
                            {message}
                            <br><br>
                            You can now close this window. The podcast pipeline will continue automatically.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="error-container">
                        <div class="big-emoji">❌</div>
                        <div class="status-text">Error Processing Approval</div>
                        <div class="details-text">
                            {message}
                            <br><br>
                            Please contact support if you continue to experience issues.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        # Invalid token
        st.markdown("""
        <div class="error-container">
            <div class="big-emoji">🔒</div>
            <div class="status-text">Invalid Token</div>
            <div class="details-text">
                The approval token is invalid or corrupted. Please use the link from your approval email.
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #666;'>Podcast Generation System © 2024</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
