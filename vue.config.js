module.exports = {
  pluginOptions: {
    s3Deploy: {
      registry: undefined,
      awsProfile: 'ams',
      region: 'ap-southeast-1',
      bucket: 'ika.pigimaru.com',
      createBucket: true,
      staticHosting: true,
      staticIndexPage: 'index.html',
      staticErrorPage: 'index.html',
      assetPath: 'dist',
      assetMatch: '**',
      deployPath: '/',
      acl: 'public-read',
      pwa: false,
      enableCloudfront: false,
      uploadConcurrency: 5,
      pluginVersion: '3.0.0'
    }
  }
}
