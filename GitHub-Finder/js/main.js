$(document).ready(function () {
  $('#searchUser').on('keyup', function (e) {
    let username = e.target.value;

    $.ajax({
      url: 'https://api.github.com/users/' + username,
      data: {
        client_id: 'b9315bcd5a07fcd759d8',
        client_secret: 'a2b698bf7e7c02f898197cf136d1a41f704ca8e4'
      }
    }).done(function (user) {
      $.ajax({
        url: 'https://api.github.com/users/' + username + '/repos',
        data: {
          client_id: 'b9315bcd5a07fcd759d8',
          client_secret: 'a2b698bf7e7c02f898197cf136d1a41f704ca8e4',
          sort: 'created: asc',
          per_page: 5
        }
      }).done(function (repos) {
        $.each(repos, function (index, repo) {
          $('#repos').append(`
            <div class="card my-2 bg-success">
              <div class="row">
                <div class="col-md-7 py-2">
                  <strong>${repo.name}</strong>: ${repo.description}
                </div>
                <div class="col-md-3 py-2">
                  <span class="badge badge-info align-items-center">Stars: ${repo.stargazers_count}</span>
                  <span class="badge badge-dark align-items-center">Forks: ${repo.forks_count}</span>
                  <span class="badge badge-primary align-items-center">Watchers: ${repo.watchers_count}</span>
                </div>
                <div class="col-md-2 py-2 align-items-center">
                  <a href="${repo.html_url}" target="_blank" class="btn btn-danger btn-sm">Repo Page</a>
                </div>
              </div>
            </div>
          `);
        });
      });
      $('#profile').html(`
        <div class="card border-primary bg-warning mb-3" style="max-width: 100rem;">
          <div class="card-header text-primary"><h3>${user.name}</h3></div>
          <div class="card-body">
            <div class="row">
            <div class="col-md-3">
              <img class="img-thumbnail avatar" src="${user.avatar_url}">
              <a target="_blank" class="btn btn-primary btn-block" href="${user.html_url}">View Profile</a>
            </div>
            <div class="col-md-9">
              <span class="badge badge-dark">Public Repos: ${user.public_repos}</span>
              <span class="badge badge-primary">Public Gists: ${user.public_gists}</span>
              <span class="badge badge-success">Followers: ${user.followers}</span>
              <span class="badge badge-info">Following: ${user.following}</span>
              <br><br>
              <ul class="list-group">
                <li class="list-group-item bg-danger">Company: ${user.company}</li>
                <li class="list-group-item bg-danger">Website: <a href="${user.blog}" target="_blank">${user.blog}</a></li>
                <li class="list-group-item bg-danger">Location: ${user.location}</li>
                <li class="list-group-item bg-danger">Member Since: ${user.created_at}</li>
              </ul>
              </div>
            </div>
          </div>
        </div>
        <h3 class="page-header text-warning">Latest Repos</h3>
        <div id="repos"></div>
        `);
    });
  });
});
