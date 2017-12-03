'''

Copyright (c) 2017, Vanessa Sochat, All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''

from shub.logger import bot
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from shub.plugins.globus.utils import get_client
from django.urls import reverse
from django.contrib import messages
from shub.plugins.globus.utils import associate_user

@login_required
def globus_login(request):
    '''
       Associate the logged in user with a globus account based on email.
       If the association doesn't exist, create it. Redirect to transfer
       page.
    '''

    # redirect_uri = reverse('globus_login')
    redirect_uri = "http://localhost/globus/login/"

    client = get_client()
    client.oauth2_start_flow(redirect_uri,
                             refresh_tokens=True)

    # First step of authentication flow - we need code
    if "code" not in request.GET:
        auth_uri = client.oauth2_get_authorize_url()
        return redirect(auth_uri)

    else:

        # Second step of authentication flow - we need to ask for token  
        code = request.GET.get('code')
        user = associate_user(request.user, 
                              client=client, 
                              code=code)

    return redirect('globus_transfer')


@login_required
def globus_transfer(request):
    '''
    '''
    context = {'user': request.user}
    return render(request, 'globus/transfer.html', context)